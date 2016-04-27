from structure_fetcher import metadata_storage_path, update_metadata
import structure_fetcher as sf
import pydrive.files

from control.constants import FILE_PATH_SEPARATOR, ENCRYPTED_FLAG, DECRYPTED_TITLE
from encryption.encryptor import Encryptor
import file_object
import secrets


class FileTreeState:
    def __init__(self, current_path=FILE_PATH_SEPARATOR):
        self.file_tree = sf.tree()
        self.currentNode = self.file_tree
        self.currentNodeID = "root"
        self.currentPath = current_path
        self.valid = True

        # Load metadata.
        meta_data_list = update_metadata()

        sf.convert_list_to_tree(self.file_tree, meta_data_list, 'root', self.file_tree)

        self.rootNode = self.file_tree

        # Set up encryptor.
        self.encryptor = Encryptor(secrets.password)

    def get_current_contents(self, type=0, name=None):
        """
        Returns the file objects contained in the current folder.
        Args:
            type: integer, 0 for all files, 1 for files, 2 for folders.

        Returns:
            list
        """
        if self.valid:
            output = []
            for key in self.currentNode.keys():
                current_el = self.currentNode[key]
                if not isinstance(current_el, pydrive.files.GoogleDriveFile):
                    continue
                if type == 1 and sf.is_folder(current_el) or \
                                        type == 2 and not sf.is_folder(current_el):
                    continue

                output.append(current_el)
            if name:
                for element in output:
                    if element['title'] == name:
                        return file_object.FileObject(element)
                return None
            return output

        else:
            return False

    def get_current_element(self):
        if self.valid:
            return file_object.FileObject(self.currentNode)
        else:
            return False

    def get_names(self, type=0):
        contents = self.get_current_contents(type)
        # return [(x[DECRYPTED_TITLE], x) if DECRYPTED_TITLE in x else (x['title'], x) for x in contents]
        return [y[DECRYPTED_TITLE] if DECRYPTED_TITLE in y else y['title'] for y in contents]

    def change_path(self, new_folder):
        if new_folder == ".":
            return True  # Do nothing.
        elif new_folder == "..":
            # Update path.
            new_path_parts = self.currentPath.split(FILE_PATH_SEPARATOR)[:-1]
            new_path = FILE_PATH_SEPARATOR.join(new_path_parts)

            if not new_path:
                new_path = FILE_PATH_SEPARATOR

            self.currentPath = new_path

            # Update current node.
            self.currentNode = self.currentNode["parent"]

        else:
            # Check if current element is folder.

            # Check if element exists.
            new_object = self.get_current_contents(0, new_folder)

            if new_object:
                self.currentNodeID = new_object.get_id()
                self.currentNode = self.currentNode[self.currentNodeID]

                path_parts = self.currentPath.split(FILE_PATH_SEPARATOR)
                path_parts.append(new_folder)
                if path_parts[1] == '':
                    del path_parts[1]
                self.currentPath = FILE_PATH_SEPARATOR.join(path_parts)

                # Decrypt all file names.
                # self._decrypt_file_names_in_current_folder()

                return True

            else:
                return False

    def get_current_path(self):
        return self.currentPath

        # TODO implement additional accessors to deal with encrypted names.
        #   If encrypted name encountered add attribute indicating that it it is encoded, and add the decoded name.

    def navigate(self, path):
        # Reset current node.
        self.currentNode = self.rootNode
        self.currentNodeID = "root"
        self.currentPath = FILE_PATH_SEPARATOR
        self.valid = True

        split_path = path.split(FILE_PATH_SEPARATOR)[1:]
        if split_path[-1] == '':
            split_path = split_path[:-1]
        for new_folder in split_path:
            self.valid = self.change_path(new_folder) != False
            if not self.valid:
                break

        return self

    def _decrypt_file_names_in_current_folder(self):
        for file_id, file_object in self.currentNode.iteritems():
            title = file_object["title"]

            if ENCRYPTED_FLAG not in file_object:
                try:
                    decrypted_title = self.encryptor.decrypt(title, string=True)
                    file_object[ENCRYPTED_FLAG] = True
                    file_object[DECRYPTED_TITLE] = decrypted_title

                except Exception as e:
                    file_object["encrypted"] = False
