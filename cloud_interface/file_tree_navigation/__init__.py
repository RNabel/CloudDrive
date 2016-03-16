from structure_fetcher import metadata_storage_path, update_metadata
import structure_fetcher as sf
import pydrive.files


class FileTreeState:
    def __init__(self, currentPath="/"):
        self.file_tree = sf.tree()
        self.currentNode = self.file_tree

        self.currentNodeID = "root"
        self.currentPath = "/"

        # Load metadata.
        meta_data_list = update_metadata()

        sf.convert_list_to_tree(self.file_tree, meta_data_list, 'root')

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

    def get_names(self, type=1):
        contents = self.get_current_contents(type)
        return [x['title'] for x in contents]

    def change_folder(self, new_folder):
        pass


if __name__ == "__main__":
    ftree = FileTreeState()
    print ftree
    print ftree.get_names(0)
    print ftree.get_names(1)
    print ftree.get_names(2)
