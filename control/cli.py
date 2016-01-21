import os
from cloud_interface import file_sync as cd


def print_startup_message():
    """

    Returns: What the user wishes to do.
        "sync" synchronize state of folder with Google Drive.
    """
    available_options = ['a', 'b', 'c']

    print "Welcome to CloudDrive!\n\n"
    while True:
        print "Please choose from the below options:\n" \
              "a) Upload a folder.\n" \
              "b) Upload a file.\n" \
              "c) Fetch all meta-data."
        chosen_option = raw_input()

        if chosen_option in available_options:
            break

    return chosen_option


def print_upload_file():
    print "Please enter the path you wish to upload."

    while True:
        path = raw_input()
        path = "/home/robin/PycharmProjects/CloudDrive/DESIGN.md"

        if os.path.exists(path):
            break
        else:
            print "The path you entered does not exist. Please re-enter the path."

    print "Uploading file..."
    cd.sync_file(path, None)
    print "The file {} was uploaded now... Success!".format(path)


def print_fetch_metadata():
    print "Fetching meta-data..."
    metadata = cd._fetch_all_file_info(None)
    print "Downloaded meta-data."
    print metadata


def start_cli():
    chosen_options = print_startup_message()

    if chosen_options == 'b':  # Upload a file.
        print_upload_file()
    if chosen_options == 'c':
        print_fetch_metadata()


if __name__ == "__main__":
    start_cli()
