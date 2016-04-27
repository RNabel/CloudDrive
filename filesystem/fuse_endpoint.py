#!/usr/bin/env python

from __future__ import with_statement

import os
import errno
import stat

from fuse import FUSE, FuseOSError, Operations

from cloud_interface import file_tree_navigation
from control import constants


class GDriveFuse(Operations):
    """
    Bundles all functionality of the fuse system.
    """

    def __init__(self, root):
        self.root = root
        self.file_tree_navigator = file_tree_navigation.FileTreeState('/')

    # Helpers
    # =======

    def _log(self, text):
        print(text)

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        self._log(u"access called with {} {}".format(path, mode))
        # full_path = self._full_path(path)
        # if not os.access(full_path, mode):
        #     raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        self._log(u"chmod called with {} {}".format(path, mode))
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        self._log(u"chown called with {} {} {}".format(path, uid, gid))
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        self._log(u"getattr called with {}".format(path))
        file_obj = self.file_tree_navigator.navigate(path).get_current_element()
        if file_obj and path != '/':
            st_fixed = dict({
                'st_ctime': 1461248557.862982,
                'st_mtime': 1461248557.7105043,
                'st_nlink': 1,
                'st_mode': stat.S_IFREG,
                'st_size': 399,
                'st_gid': 10030,
                'st_uid': 17640,
                'st_atime': 1461248577.5776684
            })

            # Reference document [here](https://docs.python.org/2/library/stat.html)
            # Set size.
            st_fixed['st_size'] = 1000

            # Set access rights
            is_folder = file_obj.is_folder()
            if is_folder:
                st_fixed['st_mode'] = stat.S_IFDIR
            else:
                st_fixed['st_mode'] = stat.S_IFREG
            # Grant full permissions.
            st_fixed['st_mode'] |= stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO

            # Set last status change time.
            st_fixed['st_ctime'] = 1461787306

            # Set last access time
            st_fixed['st_mtime'] = 1461787306
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
            return dict()

    def readdir(self, path, fh):
        self._log(u"readdir called with {} {}".format(path, fh))

        dirents = ['.', '..']
        dirents.extend(self.file_tree_navigator.navigate(path).get_names())
        for r in dirents:
            yield r

    def readlink(self, path):
        self._log(u"readlink called with {}".format(path))

        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    # Creates a special or ordinary file - used by touch and similar.
    def mknod(self, path, mode, dev):
        self._log(u"mknod called with {}".format(str(path), str(mode), str(dev)))
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        self._log(u"rmdir called with {}".format(str(path)))
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        self._log(u"mkdir called with {} {}".format(str(path), str(mode)))
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        self._log(u"statfs called with {}".format(str(path)))
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                                                         'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files',
                                                         'f_flag',
                                                         'f_frsize', 'f_namemax'))

    def unlink(self, path):
        self._log(u"unlink called with {}".format(str(path)))
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        self._log(u"symlink called with {} {}".format(str(name), str(target)))
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        self._log(u"rename called with {} {}".format(str(old), str(new)))

        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        self._log(u"link called with {} {}".format(str(target), str(name)))
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        self._log(u"utimens called with {} {}".format(str(path), str(times)))

        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        # Check if file is present in cache and download as necessary.
        curr_el = self.file_tree_navigator.navigate(path).get_current_element()
        file_name = os.path.basename(path)

        cached_file_path = constants.DECRYPTED_FOLDER_PATH + constants.FILE_PATH_SEPARATOR + file_name  # TODO update.

        # Download file if not present.
        if not os.path.exists(cached_file_path):
            curr_el.download_to(cached_file_path)

        # full_path = self._full_path(path)
        return os.open(cached_file_path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        fh = self.open(path, 0)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)


def main(mountpoint, root):
    FUSE(GDriveFuse(root), mountpoint, nothreads=True, foreground=True)


if __name__ == '__main__':
    mountpoint = '/cs/scratch/rn30/mnt'
    root = '/cs/home/rn30/Downloads'
    main(mountpoint, root)
