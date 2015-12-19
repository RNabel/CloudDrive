# Code used to get file system structure from Google Drive account.
import pprint

from cloud_interface import drive
from collections import defaultdict


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
def download_file_list():
    global fcb_list, fcb_dict
    # Download metadata of all files.
    fcb_list = drive.ListFile({'q': "trashed=false"}).GetList()

    # Read all files into dictionary.
    fcb_dict = dict()
    for file1 in fcb_list:
        fcb_dict[file1['id']] = file1


# Conversion.
# TODO convert into tree.
def _get_children_from_list(parent_id):
    if parent_id:
        return [x for
                x in fcb_list
                if parent_id in [y['id'] for y in x['parents']]]
    else:  # If no parent_id specified return all files with root as parent.
        return [x for x in fcb_list if len(x['parents']) and len([y for y in x['parents'] if y['isRoot'] == True])]


def _get_folders_from_list(file_list):
    return (x for x in fcb_list if x.metadata['mimeType'] == u"application/vnd.google-apps.folder")


def convert_list_to_tree(tree_node, parent_id):
    # Get children of parents.
    children = _get_children_from_list(parent_id)

    for child in children:
        # Add to current tree node.
        if _is_folder(child):  # Iterative call if folder.
            # Store reference to folder object in special field.
            tree_node[child['id'] + "_folder"] = child
            convert_list_to_tree(tree_node[child['id']], child['id'])
        else:
            tree_node[child['id']] = child


def _is_folder(file):
    return file.metadata['mimeType'] == u"application/vnd.google-apps.folder"


# Accessor methods.
# TODO
def get_children(identifier, isPath):
    # Either get children based on identifier, or on path.
    pass


def pretty_print_tree(tree):
    pprint.pprint({k: dict(v) for k, v in dict(tree).items()})


def _dicts(t): return {k: _dicts(dict(t[k])) for k in t}


if __name__ == '__main__':
    download_file_list()
    convert_list_to_tree(file_tree, None)
    pretty_print_tree(file_tree)
