#!/usr/bin/env python

from __future__ import with_statement

import errno
import os
import stat
import uuid

from fuse import FUSE, FuseOSError, Operations

from cloud_interface import file_tree_navigation, downloader, uploader
import decrypted_data_storage


class GDriveFuse(Operations):
    """
    Bundles all functionality of the fuse system.
    """

    def __init__(self, temp_storage_path):
        self.file_tree_navigator = file_tree_navigation.FileTreeState()
        self.open_file_table = {}
        self.open_file_table_flags = {}

        self.downloader = downloader.Downloader()
        self.uploader = uploader.Uploader()
        self.decrypted_buffer = decrypted_data_storage.DecryptedDataStorage(decrypted_folder_path=temp_storage_path)

        self._log("Fuse loaded.")

    # Helpers
    # =======

    def _log(self, text):
        print(text)

    def _open_file(self, path, fh_id=None):
        # Check if file is present in cache and download as necessary.
        if fh_id and fh_id not in self.open_file_table:
            flags = self.open_file_table_flags[fh_id]
            self.open_file_table[fh_id] = self.file_tree_navigator.open_file(path, flags)
            # self.open_file_table[fh_id] = self.downloader.download_file(path, self.file_tree_navigator, fh_id, flags)
            return self.open_file_table[fh_id]

        else:
            return self.file_tree_navigator.open_file(path, 0)
            # return self.downloader.download_file(path, self.file_tree_navigator, fh_id, 0)

    def _create_file_handle(self):
        fh = uuid.uuid4().int
        fh >>= 96  # Convert 128-bit UUID into 32-bit int.
        return fh

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        self._log(u"access called with {} {}".format(path, mode))

    def chmod(self, path, mode):
        self._log(u"chmod called with {} {}".format(path, mode))
        return 0

    def chown(self, path, uid, gid):
        self._log(u"chown called with {} {} {}".format(path, uid, gid))
        return 0

    def getattr(self, path, fh=None):
        self._log(u"getattr called with {}".format(path))
        file_obj = self.file_tree_navigator.navigate(path).get_current_element()
        if file_obj and path != '/':
            st_fixed = dict({
                'st_nlink': 1,
                'st_gid': os.getgid(),
                'st_uid': os.getuid(),
                'st_blocks': 1,
                'st_atime': 1461248577.5776684
            })

            # Reference document [here](https://docs.python.org/2/library/stat.html)
            # Set size.
            st_fixed['st_size'] = file_obj.get_size()
            st_fixed['st_blocks'] = st_fixed['st_size'] // 512 + 1
            # Set access rights
            is_folder = file_obj.is_folder()
            if is_folder:
                st_fixed['st_mode'] = stat.S_IFDIR
            else:
                st_fixed['st_mode'] = stat.S_IFREG
            # Grant full permissions.
            st_fixed['st_mode'] |= stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO

            # Set last status change time.
            st_fixed['st_ctime'] = file_obj.get_ctime()

            # Set last access time
            st_fixed['st_mtime'] = file_obj.get_mtime()
            return st_fixed

        elif path == '/':
            return dict({
                'st_ctime': 1461248557.862982,
                'st_mtime': 1461248557.7105043,
                'st_nlink': 1,
                'st_mode': 16877,
                'st_size': 399,
                'st_gid': 10030,
                'st_uid': 17640,
                'st_atime': 1461248577.5776684
            })
        else:
            raise FuseOSError(errno.ENOENT)

    def readdir(self, path, fh):
        self._log(u"readdir called with {} {}".format(path, fh))

        dirents = ['.', '..']
        dirents.extend(self.file_tree_navigator.navigate(path).get_names())
        for r in dirents:
            yield r

    def readlink(self, path):
        self._log(u"readlink called with {}".format(path))
        raise FuseOSError(errno.ENOSYS)

    # Creates a special or ordinary file - used by touch and similar.
    def mknod(self, path, mode, dev):
        self._log(u"mknod called with {}".format(str(path), str(mode), str(dev)))
        raise FuseOSError(errno.ENOSYS)

    def rmdir(self, path):
        self._log(u"rmdir called with {}".format(str(path)))
        raise FuseOSError(errno.ENOSYS)

    def mkdir(self, path, mode):
        self._log(u"mkdir called with {} {}".format(str(path), str(mode)))
        raise FuseOSError(errno.ENOSYS)

    def statfs(self, path):
        self._log(u"statfs called with {}".format(str(path)))
        raise FuseOSError(errno.ENOSYS)
        # stv = os.statvfs(full_path)
        # return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
        #                                                  'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files',
        #                                                  'f_flag',
        #                                                  'f_frsize', 'f_namemax'))

    # Deletes a file
    def unlink(self, path):
        self._log(u"unlink called with {}".format(str(path)))
        self.file_tree_navigator.navigate(path).remove_current_element()
        raise 0

    def symlink(self, name, target):
        self._log(u"symlink called with {} {}".format(str(name), str(target)))
        raise FuseOSError(errno.ENOSYS)

    def rename(self, old, new):
        self._log(u"rename called with {} {}".format(str(old), str(new)))
        raise FuseOSError(errno.ENOSYS)

    def link(self, target, name):
        self._log(u"link called with {} {}".format(str(target), str(name)))
        raise FuseOSError(errno.ENOSYS)

    def utimens(self, path, times=None):
        self._log(u"utimens called with {} {}".format(str(path), str(times)))
        # TODO implement.
        return 0

    # File methods
    # ============

    def open(self, path, flags):
        self._log(u"open called with {} {}".format(path, flags))
        # Create a new unique fh index.
        fh = self._create_file_handle()
        self.open_file_table_flags[fh] = flags
        return fh

    def create(self, path, mode, fi=None):
        self._log(u"create called with {} {} {}".format(path, mode, fi))
        flags = os.O_WRONLY | os.O_CREAT
        open_file_wrap = self.file_tree_navigator.create_file(path, flags, mode)

        fh = self._create_file_handle()
        self.open_file_table_flags[fh] = flags
        self.open_file_table[fh] = open_file_wrap

        return fh

    def read(self, path, length, offset, fh):
        self._log(u"read called with {} {} {} {}".format(path, length, offset, fh))
        try:
            fptr = self.open_file_table[fh].get_file_handle()
        except Exception as e:
            # Download the file if file handle not created.
            open_file_wrapper = self._open_file(path, fh)
            fptr = open_file_wrapper.get_file_handle()

        os.lseek(fptr, offset, os.SEEK_SET)
        return os.read(fptr, length)

    def write(self, path, buf, offset, fh):
        self._log(u"write called with {} {} {} {}".format(path, buf, offset, fh))
        try:
            fptr = self.open_file_table[fh].get_file_handle()
        except Exception as e:
            open_file_wrapper = self._open_file(path, fh)
            fptr = open_file_wrapper.get_file_handle()

        os.lseek(fptr, offset, os.SEEK_SET)
        ret_value = os.write(fptr, buf)
        self.uploader.upload_file(path, self.file_tree_navigator, fh)
        return ret_value

    def truncate(self, path, length, fh=None):
        self._log(u"truncate called with {} {} {}".format(path, length, fh))
        try:
            fptr = self.open_file_table[fh].get_file_handle()
        except Exception as e:
            fptr = self._open_file(path, fh)
        os.ftruncate(fptr, length)
        # fptr.truncate(length) has to be python file object.

    def flush(self, path, fh):
        self._log(u"flush called with {} {}".format(path, fh))
        # fptr = self.open_file_table[fh]
        # return os.fsync(fptr)
        return 0

    def release(self, path, fh):
        self._log(u"release called with {} {}".format(path, fh))
        # Delete entry in open file table.
        try:
            fptr = self.open_file_table[fh].get_file_handle()
            del self.open_file_table_flags[fh]
            del self.open_file_table[fh]
            return os.close(fptr)
        except Exception as e:
            return 0

    def fsync(self, path, fdatasync, fh):
        self._log(u"fsync called with {} {} {}".format(path, fdatasync, fh))
        fptr = self.open_file_table[fh]
        return self.flush(path, fptr)

    # Tear-down method.
    def tear_down(self):
        # Notify file tree of shut-down.
        exit_code = self.file_tree_navigator.tear_down()
        return exit_code


def main(mountpoint, temp_storage):
    gdriveFuse = GDriveFuse(temp_storage)
    FUSE(gdriveFuse, mountpoint, nothreads=True, foreground=True)
    return gdriveFuse


if __name__ == '__main__':
    mountpoint = '/cs/scratch/rn30/mnt'
    root = '/cs/home/rn30/Downloads'
    main(mountpoint)
