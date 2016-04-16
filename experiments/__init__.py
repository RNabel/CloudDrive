import base64
import os
import uu

import time

from split_file import getfilesize, splitfile
from cloud_interface import drive

SPLIT_SIZE = 20000000

upload_file_path_too_big = '/home/robin/Downloads/Silicon.Valley.S01.Season.1.720p.5.1Ch.BluRay.ReEnc-DeeJayAhmed/Silicon (copy).Valley.S01E01.720p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.txt'
upload_file_path_small = 'test.png'
upload_file_path_medium = '/home/robin/Downloads/Mary Beard -- S.P.Q.R. (2015)/test.m4b'
upload_file_path_large = '/home/robin/Downloads/Richard Dawkins - The Selfish Gene/The Selfish Gene Unabridged 1_001.mp3'

download_id_medium = ''


def main():
    # # Create temp file.
    # fptr = file(upload_file_path, 'w+')
    # fptr.write("test here")
    # fptr.flush()

    # Upload file.
    # try:
    output_file = file(upload_file_path_medium)

    file1 = drive.CreateFile({'title': 'Test_file.txt', 'mimeType': 'text/plain'})
    file1.SetContentFile(upload_file_path_medium)
    print "Uploading..."
    file1.Upload({'convert': True}),
    print "Done"

    # finally:
    # Remove temp file.
    # os.remove(fptr.name)


def wrap_lines(in_name, out_name):
    # Wrap each line with quotes.
    f_in = open(in_name)
    f_out = open(out_name, 'w+')
    for line in f_in:
        new_line = line.replace('\n', '')
        new_line = '"' + new_line + '"\n'
        f_out.write(new_line)
    f_in.close()
    f_out.close()


def upload_file(upload_file_name):
    temp_file_name = 'encoded.csv'
    # Encode file.
    base64.encode(open(upload_file_name), open(temp_file_name, 'w+'))

    # Split file.
    file_size = getfilesize(temp_file_name)
    if file_size > 13000000:
        num_split_files = splitfile(temp_file_name, 13000000)
    else:
        os.rename(temp_file_name, 'encoded_1.csv')
        num_split_files = 1

    for i in range(num_split_files):
        up_file = drive.CreateFile({'title': 'test_upload_{}.csv'.format(i), 'mimeType': 'text/csv'})
        up_file.SetContentFile('encoded_{}.csv'.format(i + 1))
        start = time.time()
        print "Uploading: {}...".format(i)
        up_file.Upload({'convert': True}),
        end = time.time()
        m, s = divmod(end - start, 60)
        print "Time taken: ", m, "m ", s, "s"

    print "Done"


def download_file(file_id, output_name):
    dl_file = drive.CreateFile({'id': file_id})
    print "Downloading"
    dl_file.GetContentFile('temp.csv', 'text/csv')
    print "Downloaded"

    # Decode file.
    base64.decode(open('temp.csv'), open(output_name, 'w+'))
    os.remove('temp.csv')
    print "Done"


if __name__ == '__main__':
    upload_file(upload_file_path_large)
