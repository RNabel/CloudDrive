"""
File that allows up and download of files using the (free) Google Spreadsheets format.
Files are converted to Base64 and up/downloaded as CSV. If the file exceeds the required size,
the file is split up and uploaded in chunks, which are reconstituted by the downloader.

File chunks are identified through a series of [Custom Properties](https://developers.google.com/drive/v2/web/properties).
"""
import base64
import os
import fileinput
import time
import uuid

from split_file import getfilesize, splitfile
from cloud_interface import drive
import upload_worker

SPLIT_SIZE = 13000000  # 13MB (13000000) is maximum.

upload_file_path_too_big = '/home/robin/Downloads/Silicon.Valley.S01.Season.1.720p.5.1Ch.BluRay.ReEnc-DeeJayAhmed/Silicon (copy).Valley.S01E01.720p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.txt'
upload_file_path_small = 'test.png'
upload_file_path_medium = '/home/robin/Downloads/Mary Beard -- S.P.Q.R. (2015)/test.m4b'
upload_file_path_large = '/home/robin/Downloads/Richard Dawkins - The Selfish Gene/The Selfish Gene Unabridged 1_001.mp3'


def upload_file(upload_file_name):
    file_name = os.path.basename(upload_file_name)
    temp_file_name = 'encoded.csv'
    # Encode file.
    base64.encode(open(upload_file_name), open(temp_file_name, 'w+'))

    # Split file.
    file_size = getfilesize(temp_file_name)
    if file_size > SPLIT_SIZE:
        num_split_files = splitfile(temp_file_name, SPLIT_SIZE)
    else:
        os.rename(temp_file_name, 'encoded_1.csv')
        num_split_files = 1

    # Start upload threads.
    start = time.time()
    threads = []
    file_id = uuid.uuid1()
    print file_id
    for i in range(num_split_files):
        up_t = upload_worker.UploadWorkerThread(kwargs=
                                                {'index': i,
                                                 'id': file_id,
                                                 'filename': file_name,
                                                 'numFileParts': num_split_files})
        up_t.start()
        threads.append(up_t)

    # Join threads, i.e. wait for completion.
    for i in threads:
        i.join()

    end = time.time()
    m, s = divmod(end - start, 60)
    print "Overall time taken: ", m, "m ", s, "s"
    return file_id


def download_file(file_id, output_name=None):
    # Get all files with uuid.
    # fcb_list = drive.ListFile({'q': 'appProperties has { key="CloudDrive" and value="%s"}' % file_id})
    fcb_list = drive.ListFile(
        {'q': "properties has { key='CloudDrive_id' and value='%s' and visibility='PUBLIC' }" % file_id}).GetList()

    if len(fcb_list) == 0:
        print "Error no file found"
        return False

    output_name = output_name or get_property('CloudDrive_filename', fcb_list[0], True)
    total_files = get_property('CloudDrive_total', fcb_list[0], True)
    assert int(total_files) == len(fcb_list)

    filenames = []
    for fi in fcb_list:
        file_name = file_id + "_" + get_property('CloudDrive_part', fi, True)
        filenames.append(file_name)
        print "Downloading"
        fi.GetContentFile(file_name, mimetype='text/csv')
        print "Downloaded"

    # Merge file.
    filenames.sort()
    merge_files(file_id, filenames)

    # Delete temp files.
    for f in filenames:
        os.remove(f)

    # Decode file.
    base64.decode(open(file_id), open(output_name, 'w+'))

    # Delete temp file.
    os.remove(file_id)
    print "Done"


# File functions.
def merge_files(output_name, filenames):
    fin = fileinput.input(filenames)
    with open(output_name, 'w') as fout:
        for line in fin:
            fout.write(line)

    fin.close()


# GoogleDriveFile accessors.
def get_property(name, file_obj, return_value=False):
    elements = filter(lambda x: x['key'] == name, file_obj.get('properties'))
    returnObj = elements[0] if len(elements) else None

    # Return the value if requested.
    if returnObj and return_value:
        returnObj = returnObj['value']
    return returnObj


if __name__ == '__main__':
    # print upload_file(upload_file_path_medium)
    download_file('c634a2bc-04d2-11e6-b18e-5ce0c598f03f')
