import base64
import os

import time

from split_file import getfilesize, splitfile
from cloud_interface import drive
import upload_worker

SPLIT_SIZE = 3000000  # 13MB (13000000) is maximum.

upload_file_path_too_big = '/home/robin/Downloads/Silicon.Valley.S01.Season.1.720p.5.1Ch.BluRay.ReEnc-DeeJayAhmed/Silicon (copy).Valley.S01E01.720p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.txt'
upload_file_path_small = 'test.png'
upload_file_path_medium = '/home/robin/Downloads/Mary Beard -- S.P.Q.R. (2015)/test.m4b'
upload_file_path_large = '/home/robin/Downloads/Richard Dawkins - The Selfish Gene/The Selfish Gene Unabridged 1_001.mp3'


def main():
    output_file = file(upload_file_path_medium)

    file1 = drive.CreateFile({'title': 'Test_file.txt', 'mimeType': 'text/plain'})
    file1.SetContentFile(upload_file_path_medium)
    print "Uploading..."
    file1.Upload({'convert': True}),
    print "Done"


def upload_file(upload_file_name):
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
    for i in range(num_split_files):
        up_t = upload_worker.UploadWorkerThread(kwargs={'index': i})
        up_t.start()
        threads.append(up_t)

    # Join threads, i.e. wait for completion.
    for i in threads:
        i.join()

    end = time.time()
    m, s = divmod(end - start, 60)
    print "Overall time taken: ", m, "m ", s, "s"


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
    upload_file(upload_file_path_medium)
