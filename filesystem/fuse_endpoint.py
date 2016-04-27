#!/usr/bin/env python

from __future__ import with_statement

import os
import errno
import stat


from fuse import FUSE, FuseOSError, Operations


class GDriveFuse(Operations):
    """
    Bundles all functionality of the fuse system.
    """

    def __init__(self, root):
        self.root = root

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
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

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
        full_path = self._full_path(path)
        st = os.lstat(full_path)
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

        if path == u'/':
            st_fixed['st_mode'] = 16877

        tmp = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                                                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size',
                                                        'st_uid'))
        return st_fixed

    def readdir(self, path, fh):
        print("readdir called with {} {}".format(path, fh))

        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
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
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
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
