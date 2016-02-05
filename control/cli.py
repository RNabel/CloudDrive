import os
import sys
import argparse

from cloud_interface import file_sync as cd

LINE_START_LOCAL = "$l "
LINE_START_REMOTE = "$r "

current_remote_path = "/"
current_rem_dir_id = "root"
current_local_path = os.path.expanduser("~")
os.chdir(current_local_path)

current_mode_local = True

# Mapping of commands to help text.
available_options = {
    'help': 'Shows this message',
    'cd': 'Enter a folder.',
    'ls': 'Show folder contents.',
    'pwd': 'Display current working directory',
    'up': 'Uploads a file or folder.',
    'dl': 'Download file or folder from remote.',
    'sw': 'Switch between local and remote storage.',
    'exit': 'End the current session.'
}


def help_handler(user_input):
    print "Some help here..."


def cd_handler(user_input):
    global current_local_path

    if current_mode_local:
        if len(user_input) < 2:
            print "cd: incorrect number of arguments."
            print "usage: cd PATH."
            return False

        folder_name = " ".join(user_input[1:])
        full_folder_path = current_local_path + "/" + folder_name

        if os.path.exists(full_folder_path) \
                and not os.path.isfile(full_folder_path):

            current_local_path = full_folder_path
            os.chdir(current_local_path)
        else:
            print "No such folder: {}".format(folder_name)

    else:
        print "cd is not implemented for remote storage yet."


def ls_handler(user_input):
    if current_mode_local:
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        folders = [f for f in os.listdir('.') if not os.path.isfile(f)]
        output_string = ""
        if files:
            output_string += "Files:\n{}{}".format(" ".join(files), "\n" if folders else "")
        if folders:
            output_string += "Folders:\n{}".format(" ".join(folders))

        print output_string
    else:
        # Fetch all meta data from current parent.
        metadata = cd._fetch_all_file_info(current_rem_dir_id, None)

        # Find all folders. TODO use structure fetcher for this.

        # Find all files.
        print "ls entered yo in remote mode."


def pwd_handler(user_input):
    if current_mode_local:
        print current_local_path
    else:
        print current_remote_path


def up_handler(user_input):
    print "up entered yo."


def dl_handler(user_input):
    print "dl entered yo."


def sw_handler(user_input):
    global current_mode_local

    current_mode_local = not current_mode_local


def exit_handler(user_input):
    print "Session ended."
    exit(0)


command_handlers = {
    'help': help_handler,
    'cd': cd_handler,
    'ls': ls_handler,
    'pwd': pwd_handler,
    'up': up_handler,
    'dl': dl_handler,
    'sw': sw_handler,
    'exit': exit_handler
}


def print_startup_message():
    """
    Welcome message of the script making it possible
    Returns: What the user wishes to do.
        "sync" synchronize state of folder with Google Drive.
    """

    print "Welcome to CloudDrive!\n\n"


def print_line_start():
    """
    Prints the beginning of each command-enabled line, to indicate whether current mode is local or remote.
    Returns: None
    """
    if current_mode_local:
        start = LINE_START_LOCAL
    else:
        start = LINE_START_REMOTE

    sys.stdout.write(start)


def execute_command():
    print_line_start()

    input_string = raw_input()
    split_input = input_string.split(" ")
    command = split_input[0]

    if command in command_handlers.keys():
        command_handlers[command](split_input)  # execute command if command found.
        return True
    else:
        # Print help message if command entered incorrectly.
        print "Command {} not found. Type help to get an overview of all possible commands.".format(command)
        return False


# --- Miscellaneous functionality. ---
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
    metadata = cd._fetch_all_file_info('root', None)
    print "Downloaded meta-data."
    print metadata


# --- Entry point. ---
def run_cli():
    print_startup_message()

    while True:
        success = execute_command()
        #
        # if chosen_option == 'b':  # Upload a file.
        #     print_upload_file()
        # if chosen_option == 'c':
        #     print_fetch_metadata()


if __name__ == "__main__":
    run_cli()
