import threading
import os
import strict_rfc3339

from cloud_interface import drive
import structure_fetcher as sf
import pydrive.files

from cloud_interface.file_tree_navigation.about_object import AboutObject
from control.constants import FILE_PATH_SEPARATOR, ENCRYPTED_FLAG, DECRYPTED_TITLE
import control.constants as constants
from encryption.encryptor import Encryptor
import file_object
import meta_data
import open_file_wrapper
import filesystem.decrypted_data_storage
import secrets


class FileTreeState:
    def __init__(self, current_path=FILE_PATH_SEPARATOR):
        self.file_tree = sf.tree()
        self.currentNode = self.file_tree
        self.currentNodeID = "root"
        self.currentPath = current_path
        self.valid = True

        self.file_cache = filesystem.decrypted_data_storage.DecryptedDataStorage()

        # Load metadata.
        self.metadata_wrapper = meta_data.MetaDataWrapper(self.file_tree)
        meta_data_list = self.metadata_wrapper.load()

        if meta_data_list is not True:
            sf.convert_list_to_tree(self.metadata_wrapper.file_tree,
                                    meta_data_list, 'root',
                                    self.metadata_wrapper.file_tree)

        self.file_tree = self.metadata_wrapper.file_tree
        self.rootNode = self.file_tree

        # Set up encryptor.
        self.encryptor = Encryptor(secrets.password)

        # Set up file tree updater.
        self.update_thread = FileTreeUpdater(self)
        # self.update_thread.start()

    def get_current_contents(self, type=0, name=None):
        """
        Returns the file objects contained in the current folder.
        Args:
            type: integer, 0 for all files, 1 for files, 2 for folders.

        Returns:
            file_object.FileObject | list
        """
        if self.valid:
            output = []
            for key in [x for x in self.currentNode.keys() if x not in ['parent', 'self']]:
                current_el = self.currentNode[key]
                # Ignore object if incorrect instance type.
                if not isinstance(current_el, pydrive.files.GoogleDriveFile):
                    continue

                # Check if is correct file (i.e. mimetype, ignoring Google Drive specific file types).
                is_file = sf.is_file(current_el)
                is_folder = sf.is_folder(current_el)

                if is_file or is_folder:
                    if type == 0 or \
                                            type == 1 and is_file or \
                                            type == 2 and is_folder:
                        output.append(current_el)
                else:
                    continue

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
            if isinstance(self.currentNode, pydrive.files.GoogleDriveFile):
                return file_object.FileObject(self.currentNode)
            elif isinstance(self.currentNode, dict):
                return file_object.FileObject(self.currentNode['self'])
        else:
            return False

    def get_names(self, type=0):
        contents = self.get_current_contents(type)
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
            return True

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

    def add_file_entry(self, file_obj, is_folder=False):
        file_id = file_obj.get_id()
        if is_folder:
            self.currentNode[file_id]['parent'] = self.currentNode
            self.currentNode[file_id]['self'] = file_obj.file
            self.currentNode[file_id + "_folder"] = file_obj.file
        else:
            self.currentNode[file_id] = file_obj.file
        return self

    def add_file_entry_id(self, file_obj):
        print "Adding file based on id."
        return self

    def update_file_entry_id(self, file_obj):
        print "Updating file entry based on id."
        return self

    def remove_current_element(self):
        curr_el = self.get_current_element()
        curr_id = curr_el.get_id()

        # Remove the part of the element from the file tree.
        if curr_el.is_file() and curr_id in self.file_tree['parent']:
            # Remove from tree structure
            del self.file_tree['parent'][curr_id]
        elif curr_el.is_folder():  # If folder
            del self.currentNode['parent'][curr_id]
            del self.currentNode['parent'][curr_id + "_folder"]
        else:
            print Exception("remove_current_element failed as element not present")

        # Remove the backed file.
        curr_el.remove()

    def set_utime(self, times):
        curr_el = self.get_current_element()
        pass

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

    # File access points.
    def open_file(self, path, flags):
        """
        Opens a file and returns an OpenFileWrapper object
        Args:
            path: The path to the file
            flags: The flags to open the file with
        Returns:
            OpenFileWrapper
        """
        # Resolve the path.
        current_element = self.navigate(path).get_current_element()

        # Request open file handle from cache.
        os_fptr, cache_state = self.file_cache.open_file(current_element, flags)

        # Wrap up all components.
        open_file_wrap = open_file_wrapper.OpenFileWrapper(current_element, os_fptr, cache_state)

        return open_file_wrap

    def create_file(self, path, flags, mode):
        dir_name = os.path.dirname(path)
        file_name = os.path.basename(path)
        folder_el = self.navigate(dir_name).get_current_element()

        # Create new backing store object.
        folder_id = folder_el.get_id()
        new_file = file_object.FileObject(file_name=file_name, parent_id=folder_id)
        fptr, cache_state = self.file_cache.create_file(new_file, mode, flags)

        open_file_wrap = open_file_wrapper.OpenFileWrapper(new_file, fptr, cache_state)

        # Add object to file tree. USING GoogleDriveFile.
        self.add_file_entry(new_file)

        return open_file_wrap

    def create_folder(self, path, mode):
        dir_name = os.path.dirname(path)
        folder_name = os.path.basename(path)
        par_folder_el = self.navigate(dir_name).get_current_element()

        par_fol_id = par_folder_el.get_id()
        new_folder = file_object.FileObject(file_name=folder_name, parent_id=par_fol_id, is_folder=True)
        self.add_file_entry(new_folder, is_folder=True)
        return new_folder

    def read(self):
        pass

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

    def tear_down(self):
        # End worker threads.
        try:
            self.update_thread.set_stop_flag()
            self.update_thread.join()
        except Exception as e:
            pass

        # Save metadata.
        print "Saving metadata."
        self.metadata_wrapper.save()
        return 0


class FileTreeUpdater(threading.Thread):
    def __init__(self, file_tree_navigator):
        """

        Args:
            file_tree_navigator(FileTreeState): The current tree state.
        """
        threading.Thread.__init__(self)
        self.stop = threading.Event()
        self.loop = threading.Event()
        self.file_tree_navigator = file_tree_navigator

    def set_stop_flag(self):
        self.stop.set()
        self.loop.set()

    def run(self):
        while not self.stop.is_set():
            last_update = self.file_tree_navigator.metadata_wrapper.last_update

            self.file_tree_navigator.metadata_wrapper.set_update_time_to_now()
            fcb_list = drive.ListFile(
                {'q': 'modifiedDate >="{}" and trashed=false'.format(last_update)}
            ).GetList()
            self.process_changes(fcb_list, last_update)

            print "There were {} changes.".format(len(fcb_list))
            self.loop.wait(constants.UPDATE_INTERVAL)

    def process_changes(self, fcb_list, last_update):
        last_update = strict_rfc3339.rfc3339_to_timestamp(last_update)
        for element in fcb_list:
            element = file_object.FileObject(element)
            # Handle new files
            creation_time = element.get_ctime()
            if creation_time > last_update:
                # Handle new file.
                print "New file found: {}".format(element.get_name())
                self.file_tree_navigator.add_file_entry_id(element)
            else:
                # Handle changed file.
                print "Changed file found: {}".format(element.get_name())
                self.file_tree_navigator.update_file_entry_id(ek)
