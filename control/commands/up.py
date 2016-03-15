import sys
import os
import cloud_interface.file_sync as file_sync
import cloud_interface.structure_fetcher as sf

from control.commands import current_local_path, current_remote_dir_id, get_current_folder_contents


def handler(user_input):
    # Check if file exists and is file.
    file_name = " ".join(user_input[1:])
    file_path = current_local_path + "/" + file_name

    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Upload file here.
        print "Uploading file..."
        file_sync.sync_file(file_path, current_remote_dir_id)
        print "The file {} was uploaded - Success!".format(file_path)

    elif file_name.strip() == "*":
        # Upload all files.
        print "Uploading files..."
        i = 0
        # Get all files in current local directory.
        files, folders = get_current_folder_contents(local=True)
        total = len(files)

        for name in files:
            sys.stdout.write("\rUploading {}, {} of {}".format(name, i, total))
            sys.stdout.flush()
            file_path = current_local_path + "/" + name

            file_sync.sync_file(file_path, current_remote_dir_id)

            i += 1
        sys.stdout.write("\rAll files uploaded.\n")

    else:
        print "Error could not find file {}. usage: up FILE_NAME".format(file_name)
        return False

    sf.update_metadata()
