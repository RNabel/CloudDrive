from structure_fetcher import metadata_storage_path, update_metadata
import structure_fetcher as sf
import pydrive.files

from control.constants import FILE_PATH_SEPARATOR


class FileTreeState:
    def __init__(self, currentPath="/"):
        self.file_tree = sf.tree()
        self.currentNode = self.file_tree

        self.currentNodeID = "root"
        self.currentPath = FILE_PATH_SEPARATOR

        # Load metadata.
        meta_data_list = update_metadata()

        sf.convert_list_to_tree(self.file_tree, meta_data_list, 'root', self.file_tree)

    def get_current_contents(self, type=0):
        """
        Returns the file objects contained in the current folder.
        Args:
            type: integer, 0 for all files, 1 for files, 2 for folders.

        Returns:
            list
        """

        output = []
        for key in self.currentNode.keys():
            current_el = self.currentNode[key]
            if not isinstance(current_el, pydrive.files.GoogleDriveFile):
                continue
            if type == 1 and sf.is_folder(current_el) or \
                                    type == 2 and not sf.is_folder(current_el):
                continue

            output.append(current_el)
        return output

    def get_names(self, type=0):
        contents = self.get_current_contents(type)
        return [(x['title'], x) for x in contents]

    def change_folder(self, new_folder):
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
            # Check if element exists.
            names = self.get_names(2)
            current_folder = [x for x in names if x[0] == new_folder]

            if current_folder:
                current_folder = current_folder[0]
                self.currentNodeID = current_folder[1]["id"]
                self.currentNode = self.currentNode[self.currentNodeID]

                path_parts = self.currentPath.split(FILE_PATH_SEPARATOR)
                path_parts.append(new_folder)
                if path_parts[1] == '':
                    del path_parts[1]
                self.currentPath = FILE_PATH_SEPARATOR.join(path_parts)
                return True

            else:
                return False

    def get_current_path(self):
        return self.currentPath

        # TODO implement additional accessors to deal with encrypted names.
        #   If encrypted name encountered add attribute indicating that it it is encoded, and add the decoded name.


if __name__ == "__main__":
    ftree = FileTreeState()
    ftree.change_folder("..")  # should not do anything.
    ftree.change_folder("Test_folder")
    ftree.change_folder("..")
    print "hello"
