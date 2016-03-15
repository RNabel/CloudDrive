# Holds the current state of the system.
import os
import sys
import cloud_interface.structure_fetcher as sf

current_remote_path = "/Test_folder"
current_remote_dir_id = "0B46HJMu9Db4xTUxhQ0x4WHpfVmM"
current_local_path = os.path.expanduser("~")
os.chdir(current_local_path)

current_mode_local = True
is_metadata_fetched = False

contained_folders = []
contained_files = []

# Mapping of commands to help text.
available_options = {
    'help': 'Shows this message',
    'cd': 'Enter a folder.',
    'ls': 'Show folder contents.',
    'mkdir': 'Create new folder.',
    'cwd': 'Display current working directory',
    'up': 'Uploads a file or folder.',
    'dl': 'Download file or folder from remote.',
    'sw': 'Switch between local and remote storage.',
    'exit': 'End the current session.'
}


# --- Helper methods ---
def get_current_folder_contents(local=None):
    current_mode = current_mode_local
    if local is not None:
        current_mode = local

    if current_mode:
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        folders = [f for f in os.listdir('.') if not os.path.isfile(f)]
    else:
        children = sf.get_children(current_remote_path, True)
        files = sf.filter_file_list(children, False)
        files = sf.get_titles(files)
        folders = sf.filter_file_list(children, True)
        folders = sf.get_titles(folders)

    return files, folders


def fetch_metadata():
    sys.stdout.write("Fetching meta-data from Google Drive...")
    sf.update_metadata()
    sys.stdout.write("Done!\n")
