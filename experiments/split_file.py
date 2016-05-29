import os

"""
File Splitter; code taken from: [StackOverflow Answer](http://stackoverflow.com/a/33151466/3918512)
"""


def getfilesize(filename):
    """
    Return file size in bytes.
    Args:
        filename: The name of the file.

    Returns:
        Size of file in bytes.
    """
    with open(filename, "rb") as fr:
        fr.seek(0, 2)  # move to end of the file
        size = fr.tell()
        print("getfilesize: size: %s" % size)
        return fr.tell()


def splitfile(filename, splitsize, split_file_format="{orig_file}_{id}.{orig_ext}"):
    """
    Splits a file into splitsize-sized chunks
    Args:
        split_file_format: formatting of the split files.
                    fields available: the original_file_name = {orig_file},
                                      original file ending = {orig_ext}
                                      the current index = {id}
        filename: Name of the file to be split.
        splitsize: Size of each splitted component in bytes.

    Returns:
        int - Number of file chunks.
    """
    # Open original file in read only mode
    if not os.path.isfile(filename):
        print("No such file as: \"%s\"" % filename)
        return

    filesize = getfilesize(filename)
    filenames = []
    with open(filename, "rb") as fr:
        counter = 1
        orginalfilename = filename.split(".")
        readlimit = 5000  # read 5kb at a time
        n_splits = filesize // splitsize
        print("splitfile: No of splits required: %s" % str(n_splits))
        for i in range(n_splits + 1):
            chunks_count = int(splitsize) // int(readlimit)
            data_5kb = fr.read(readlimit)  # read
            # Create split files
            print("chunks_count: %d" % chunks_count)
            chunk_file_name = split_file_format.format(id=str(counter),
                                                       orig_file=str(orginalfilename[0]),
                                                       orig_ext=str(orginalfilename[1]))
            with open(chunk_file_name, "ab") as fw:
                fw.seek(0)
                fw.truncate()  # truncate original if present
                while data_5kb:
                    fw.write(data_5kb)
                    if chunks_count:
                        chunks_count -= 1
                        data_5kb = fr.read(readlimit)
                    else:
                        break

            counter += 1
            filenames.append(chunk_file_name)

    return n_splits + 1, filenames
