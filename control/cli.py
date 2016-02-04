import os
import sys
import argparse

from cloud_interface import file_sync as cd

LINE_START_LOCAL = "$l "
LINE_START_REMOTE = "$r "

current_remote_path = "/"
current_folder_id = "root"
current_local_path = os.path.expanduser("~")
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


def help_handler(input):
    print "Some help here..."


def cd_handler(input):
    print "cd entered yo."


def ls_handler(input):
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
        print "ls entered yo in remote mode."


def pwd_handler(input):
    if current_mode_local:
        print current_local_path
    else:
        print current_remote_path


def up_handler(input):
    print "up entered yo."


def dl_handler(input):
    print "dl entered yo."


def sw_handler(input):
    global current_mode_local

    current_mode_local = not current_mode_local


def exit_handler(input):
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

    command = input_string.split(" ")[0]

    if command in command_handlers.keys():
        command_handlers[command](input_string)  # execute command if command found.
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
    metadata = cd._fetch_all_file_info(None)
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
