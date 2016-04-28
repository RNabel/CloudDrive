#!/usr/bin/env python

from __future__ import with_statement

import os
import stat
import uuid

from fuse import FUSE, FuseOSError, Operations

from cloud_interface import file_tree_navigation, downloader, uploader
from control import constants


class GDriveFuse(Operations):
    """
    Bundles all functionality of the fuse system.
    """

    def __init__(self, root):
        self.root = root
        self.file_tree_navigator = file_tree_navigation.FileTreeState('/')
        self.open_file_table = {}
        self.open_file_table_flags = {}

        self.downloader = downloader.Downloader()
        self.uploader = uploader.Uploader()

    # Helpers
    # =======

    def _log(self, text):
        print(text)

    def _cache_file(self, path, fh_id):
        # Check if file is present in cache and download as necessary.
        if fh_id not in self.open_file_table:
            flags = self.open_file_table_flags[fh_id]
            self.open_file_table[fh_id] = self.downloader.download_file(path, self.file_tree_navigator, fh_id, flags)

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        self._log(u"access called with {} {}".format(path, mode))

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
        # Create a new unique fh index.
        fh = uuid.uuid4().int
        fh >>= 96
        self.open_file_table_flags[fh] = flags
        return fh

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        try:
            fptr = self.open_file_table[fh]
        except Exception as e:
            # Download the file if file handle not created.
            self._cache_file(path, fh)
            fptr = self.open_file_table[fh]

        os.lseek(fptr, offset, os.SEEK_SET)
        return os.read(fptr, length)

    def write(self, path, buf, offset, fh):
        try:
            fptr = self.open_file_table[fh]
        except Exception as e:
            self._cache_file(path, fh)
            fptr = self.open_file_table[fh]

        os.lseek(fptr, offset, os.SEEK_SET)
        ret_value = os.write(fptr, buf)
        self.uploader.upload_file(path, self.file_tree_navigator, fh)
        return ret_value

    def truncate(self, path, length, fh=None):
        try:
            fptr = self.open_file_table[fh]
        except Exception as e:
            self._cache_file(path, fh)
            fptr = self.open_file_table[fh]
        fptr.truncate(length)

    def flush(self, path, fh):
        fptr = self.open_file_table[fh]
        return os.fsync(fptr)

    def release(self, path, fh):
        # Delete entry in open file table.
        try:
            fptr = self.open_file_table[fh]
            del self.open_file_table_flags[fh]
            del self.open_file_table[fh]
            return os.close(fptr)
        except Exception as e:
            return 0

    def fsync(self, path, fdatasync, fh):
        fptr = self.open_file_table[fh]
        return self.flush(path, fptr)


def main(mountpoint, root):
    FUSE(GDriveFuse(root), mountpoint, nothreads=True, foreground=True)


if __name__ == '__main__':
    mountpoint = '/cs/scratch/rn30/mnt'
    root = '/cs/home/rn30/Downloads'
    main(mountpoint, root)
