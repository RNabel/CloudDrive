import os
import sys
import argparse
import rlcompleter
import readline

from cloud_interface import file_sync as cd, structure_fetcher as sf
import control.constants
from control.tools import *

LINE_START_LOCAL = "$l "
LINE_START_REMOTE = "$r "

current_remote_path = ""
current_rem_dir_id = "root"
current_local_path = os.path.expanduser("~")
os.chdir(current_local_path)

current_mode_local = True
is_metadata_fetched = False

current_contents = []

# Mapping of commands to help text.
available_options = {
    'help': 'Shows this message',
    'cd': 'Enter a folder.',
    'ls': 'Show folder contents.',
    'cwd': 'Display current working directory',
    'up': 'Uploads a file or folder.',
    'dl': 'Download file or folder from remote.',
    'sw': 'Switch between local and remote storage.',
    'exit': 'End the current session.'
}


def help_handler(user_input):
    output_string = ""

    for k, v in available_options.iteritems():
        output_string += getCyan(k) + "\t" + getRed(v) + "\n"

    sys.stdout.write(output_string)


def cd_handler(user_input):
    global current_local_path, current_remote_path, current_contents, current_rem_dir_id

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
            return False

    else:  # Remote mode.
        new_folder = " ".join(user_input[1:])
        file_path_separator = control.constants.FILE_PATH_SEPARATOR

        if new_folder == "..":
            separated_path = current_remote_path.split(file_path_separator)
            new_path = file_path_separator.join(separated_path[:-1])
            current_remote_path = new_path

        elif new_folder == ".":
            pass  # do nothing as current folder.

        else:
            # Verify path exists.
            new_path = current_remote_path + control.constants.FILE_PATH_SEPARATOR + new_folder
            file_object = sf.get_file_from_path(new_path)

            if file_object and sf.is_folder(file_object):
                current_remote_path = new_path
                current_rem_dir_id = file_object['id']
            else:
                print "The specified folder does not exist!"
                return False

    files, folders = get_current_folder_contents()
    current_contents = files + folders


def ls_handler(user_input):
    files, folders = get_current_folder_contents()

    output_string = ""
    if files:
        output_string += getYellow(u"Files:\n{}{}".format("'" + "' '".join(files) + "'", "\n" if folders else ""))
    if folders:
        output_string += getLightPurple(u"Folders:\n{}".format("'" + "' '".join(folders) + "'"))

    print output_string


def get_current_folder_contents():
    if current_mode_local:
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        folders = [f for f in os.listdir('.') if not os.path.isfile(f)]
    else:
        children = sf.get_children(current_remote_path, True)
        files = sf.filter_file_list(children, False)
        files = sf.get_titles(files)
        folders = sf.filter_file_list(children, True)
        folders = sf.get_titles(folders)

    return files, folders


def cwd_handler(user_input):
    if current_mode_local:
        print current_local_path
    else:
        print current_remote_path


# usage: up FILE_NAME
def up_handler(user_input):
    # Check if file exists and is file.
    file_name = " ".join(user_input[1:])
    file_path = current_local_path + "/" + file_name

    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Upload file here.
        print "Uploading file..."
        cd.sync_file(file_path, current_rem_dir_id)
        print "The file {} was uploaded now... Success!".format(file_path)
        return True

    else:
        print "Error could not find file {}. usage: up FILE_NAME".format(file_name)
        return False


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
    'cwd': cwd_handler,
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
        start = getRed(LINE_START_LOCAL)
    else:
        start = getCyan(LINE_START_REMOTE)

    sys.stdout.write(start)


def execute_command():
    print_line_start()

    input_string = raw_input()
    input_string.strip()

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
def fetch_metadata():
    sys.stdout.write("Fetching meta-data from Google Drive...")
    sf.update_metadata()
    is_metadata_fetched = True
    sys.stdout.write("Done!\n")


def complete(text, state, list=current_contents):
    # Ideally completion for each type of command.
    # Strip the command from text.
    text = " ".join(text.split(" ")[1:])

    for option in list:
        if option.startswith(text):
            if not state:
                return option
            else:
                state -= 1


readline.parse_and_bind("tab: complete")
readline.set_completer(complete)


# --- Entry point. ---
def run_cli():
    print_startup_message()
    fetch_metadata()

    while True:
        success = execute_command()
        #
        # if chosen_option == 'b':  # Upload a file.
        #     print_upload_file()
        # if chosen_option == 'c':
        #     print_fetch_metadata()


if __name__ == "__main__":
    run_cli()
