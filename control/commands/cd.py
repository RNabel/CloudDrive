import os

import control.commands as commands
import control.constants
from cloud_interface.file_tree_navigation import structure_fetcher as sf


def handler(user_input):
    if len(user_input) < 2:
        print "cd: incorrect number of arguments."
        print "usage: cd PATH."
        return False

    if commands.current_mode_local:
        is_folder_change_success = _handle_local_mode(user_input)

    else:  # Remote mode.
        is_folder_change_success = _handle_remote_mode(user_input)

    if is_folder_change_success:
        files, folders = commands.get_current_folder_contents()
        commands.contained_folders = folders
        commands.contained_files = files


def _handle_local_mode(user_input):
    folder_name = " ".join(user_input[1:])
    full_folder_path = commands.current_local_path + "/" + folder_name

    if os.path.exists(full_folder_path) \
            and not os.path.isfile(full_folder_path):

        if folder_name == "..":
            separated_path = commands.current_local_path.split("/")
            new_path = "/".join(separated_path[:-1])
            commands.current_local_path = new_path
        else:
            commands.current_local_path = full_folder_path

        os.chdir(commands.current_local_path)
        return True
    else:
        print "No such folder: {}".format(folder_name)
        return False


def _handle_remote_mode(user_input):
    new_folder = " ".join(user_input[1:])
    file_path_separator = control.constants.FILE_PATH_SEPARATOR

    if new_folder == "..":
        separated_path = commands.current_remote_path.split(file_path_separator)
        new_path = file_path_separator.join(separated_path[:-1])
        commands.current_remote_path = new_path

    elif new_folder == ".":
        pass  # do nothing as current folder.

    else:
        # Verify path exists.
        new_path = commands.current_remote_path + control.constants.FILE_PATH_SEPARATOR + new_folder
        file_object = sf.get_file_from_path(new_path)

        if file_object and sf.is_folder(file_object):
            commands.current_remote_path = new_path
            commands.current_remote_dir_id = file_object['id']
        else:
            print "The specified folder does not exist!"
            return False

    return True
