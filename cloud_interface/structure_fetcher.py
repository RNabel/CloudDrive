# Code used to get file system structure from Google Drive account.
import pprint
from collections import defaultdict
from cloud_interface import drive
import control.constants


# File structure.
def tree():
    """
    Returns:
        Autovififying tree

    """
    return defaultdict(tree)


file_tree = tree()
fcb_dict = dict()  # Map between ID and object.
fcb_list = None  # List returned by update call.


# Cloud functions.
def update_metadata():
    """
    Sets up or updates global variables with an update of the files stored on GDrive folder.
    Returns:
        None
    """
    global fcb_list, fcb_dict
    # Download metadata of all files.
    fcb_list = drive.ListFile({'q': "trashed=false"}).GetList()

    # Read all files into dictionary.
    fcb_dict = dict()
    for file1 in fcb_list:
        fcb_dict[file1['id']] = file1


# Conversion.
def _get_children_from_list(parent_id):
    """
    Get all children of given id from file_list object.
    Args:
        parent_id: The id of the parent, if None, falsy value or 'root' passed, returns the all children of root.

    Returns:
        List of GoogleDriveFile
    """
    if parent_id and parent_id != 'root':
        return [x for
                x in fcb_list
                if parent_id in [y['id'] for y in x['parents']]]
    else:  # If no parent_id specified return all files with root as parent.
        return [x for x in fcb_list if len(x['parents']) and len([y for y in x['parents'] if y['isRoot'] == True])]


def _get_folders_from_list(file_list):
    return (x for x in fcb_list if x.metadata['mimeType'] == u"application/vnd.google-apps.folder")


def convert_list_to_tree(tree_node, parent_id):
    """
    Recursively create file_tree.
    Args:
        tree_node: The current root node in tree.
        parent_id: The id of the current root folder.
                   (note: this is not the 'root' folder of GDrive but the
                      subfolder currently considered top of the file tree.)

    Returns:
        None
    """
    # Get children of parents.
    children = _get_children_from_list(parent_id)

    for child in children:
        # Add to current tree node.
        if is_folder(child):  # Iterative call if folder.
            # Store reference to folder object in special field.
            tree_node[child['id'] + "_folder"] = child
            convert_list_to_tree(tree_node[child['id']], child['id'])
        else:
            tree_node[child['id']] = child


def is_folder(file_object):
    return file_object.metadata['mimeType'] == u"application/vnd.google-apps.folder"


# Accessor methods.
# TODO in prog, not finished. needs some testing.
def get_children(identifier, is_path):
    if is_path:
        file_object = get_file_from_path(identifier)
        if file_object:
            folder_children = _get_children_from_list(file_object['id'])  # FIXME crashed after "cd .." command
            return folder_children
        else:
            return []

    else:
        return _get_children_from_list(identifier)


def get_file_from_path(path):
    path = path.split(control.constants.FILE_PATH_SEPARATOR)

    current_folder_id = 'root'
    current_folder = file_tree
    path = path[1:]

    for dir_name in path:
        # check if folder name exists in current folder id.
        current_folder = get_file_object_from_parent(current_folder_id, dir_name)

        if not current_folder:
            return False
        else:
            current_folder_id = current_folder['id']

    # Get all child elements of the current folder.
    return current_folder


def get_id_from_path(path):
    file_obj = get_file_from_path(path)
    return file_obj['id']


def get_file_object_from_parent(parent_id, child_name):
    # get children of parent_id
    children = _get_children_from_list(parent_id)

    # find child with given name
    file_object = _get_file_from_list(children, child_name)

    return file_object


def filter_file_list(files, want_folders):
    if want_folders:
        return [f for f in files if f.metadata['mimeType'] == u'application/vnd.google-apps.folder']
    else:
        return [f for f in files if f.metadata['mimeType'] != u'application/vnd.google-apps.folder']


def get_titles(file_list):
    return [f['title'] for f in file_list]


def _get_file_from_list(file_list, title):
    for element in file_list:
        if element['title'] == title:
            return element

    return False


def pretty_print_tree(input_tree):
    """
    Pretty print a nested default dictionary structure.
    Args:
        input_tree: The root of the nested dictionary.

    Returns:
        None
    """
    pprint.pprint({k: dict(v) for k, v in dict(input_tree).items()})


def _dicts(t): return {k: _dicts(dict(t[k])) for k in t}


if __name__ == '__main__':
    update_metadata()
    convert_list_to_tree(file_tree, 'root')
    get_file_object_from_parent('root', 'Documents')
    get_children('/Documents', True)
