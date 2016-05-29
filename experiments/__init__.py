"""
File that allows up and download of files using the (free) Google Spreadsheets format.
Files are converted to Base64 and up/downloaded as CSV. If the file exceeds the required size,
the file is split up and uploaded in chunks, which are reconstituted by the downloader.

File chunks are identified through a series of
[Custom Properties](https://developers.google.com/drive/v2/web/properties).
"""
import base64
import os
import fileinput
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from split_file import getfilesize, splitfile
import control.constants

# Set up project path.
if __name__ == '__main__':
    # Set project variable.
    control.constants.PROJECT_FOLDER = os.path.abspath("../")

from cloud_interface import drive
import download_worker
import upload_worker

SPLIT_SIZE = 13000000  # 13MB (13000000) is maximum.
MAX_DOWNLOADS = 2
MAX_UPLOADS = 2

# Test files generated with `dd if=/dev/zero of={file name} bs={size}M count=1`
upload_file_path_small = 'small.dat'
upload_file_path_medium = 'medium.dat'
upload_file_path_large = 'large.dat'


def upload_file(upload_file_name,
                temp_file_name='encoded.csv',
                split_file_format="{orig_file}_{id}.{orig_ext}",
                parent_folder_id='0B46HJMu9Db4xTUxhQ0x4WHpfVmM'):
    file_name = os.path.basename(upload_file_name)

    # Encode file.
    base64.encode(open(upload_file_name), open(temp_file_name, 'w+'))

    # Split file.
    num_split_files, file_names = splitfile(temp_file_name, SPLIT_SIZE, split_file_format)

    # Start upload threads.
    start = time.time()
    file_id = uuid.uuid1()
    thread_pool = ThreadPoolExecutor(max_workers=MAX_DOWNLOADS)

    for i in range(num_split_files):
        current_file_name = file_names[i]
        up_t = upload_worker.UploadWorker(index=i + 1,
                                          file_id=file_id,
                                          filename=file_name,
                                          parent_folder_id=parent_folder_id,
                                          total_file_num=num_split_files,
                                          upload_file_name=current_file_name)
        future = thread_pool.submit(up_t.run)

    # Wait for completion.
    thread_pool.shutdown()

    end = time.time()
    m, s = divmod(end - start, 60)
    print "Overall time taken: ", m, "m ", s, "s"
    return file_id


def download_file(file_id, output_name=None):
    # Get all files with uuid.
    fcb_list = drive.ListFile(
        {'q': "properties has { key='CloudDrive_id' and value='%s' and visibility='PUBLIC' }" % file_id}).GetList()

    if len(fcb_list) == 0:
        print "Error, file was not found."
        return False

    output_name = output_name or get_property('CloudDrive_filename', fcb_list[0], True)
    total_files = get_property('CloudDrive_total', fcb_list[0], True)
    assert int(total_files) == len(fcb_list)

    file_names = []
    thread_pool = ThreadPoolExecutor(max_workers=MAX_UPLOADS)
    futures = []
    for fi in fcb_list:
        index = get_property('CloudDrive_part', fi, True)
        uload_worker = download_worker.DownloadWorker(index=index, file_id=file_id, file_obj=fi)
        # file_names.append(uload_worker.get_file_name())

        # futures.append(thread_pool.submit(uload_worker.run))
        uload_worker.run()

    # Wait for download completion.
    # thread_pool.shutdown(wait=True)
    # ret = concurrent.futures.wait(futures)
    # print ret

    # Merge file.
    file_names.sort()
    merge_files(file_id, file_names)

    # Delete temp files.
    for f in file_names:
        os.remove(f)

    # Decode file.
    base64.decode(open(file_id), open(output_name, 'w+'))

    # Delete temp file.
    os.remove(file_id)
    print "Done"


# File functions.
def merge_files(output_name, file_names):
    fin = fileinput.input(file_names)
    with open(output_name, 'w') as fout:
        for line in fin:
            fout.write(line)

    fin.close()


# GoogleDriveFile accessor.
def get_property(name, file_obj, return_value=False):
    elements = filter(lambda x: x['key'] == name, file_obj.get('properties'))
    return_obj = elements[0] if len(elements) else None

    # Return the value if requested.
    if return_obj and return_value:
        return_obj = return_obj['value']
    return return_obj


if __name__ == '__main__':
    # print upload_file(upload_file_path_medium)
    download_file('faf03488-05ab-11e6-a401-80ee7341b961')
