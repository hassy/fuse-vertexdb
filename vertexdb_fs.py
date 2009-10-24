# FUSE interface for vertexdb
# by Hasan Veldstra

from errno import ENOENT, EACCES
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time
import os
import platform

from fuse import FUSE, Operations, LoggingMixIn

from vertexdb import VertexDb

O_ACCMODE = 3

# FIXME: ENOENT for paths that don't exist.

class VertexDbFs(Operations):

    def __init__(self):
        self.vdb = VertexDb()
        
    def getattr(self, path, fh):
        now = time() # FIXME: Get correct times.
        if self.vdb.is_dir(path):
            if platform.system() == "Darwin":
                st_nlink = self.vdb.size(path) + 2
            elif platform.system() == "Linux":
                st_nlink = self.vdb.size(path)
                
            return dict(st_mode=(S_IFDIR|0755), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=st_nlink)
        else:
            data = self.vdb.read(path)
            return dict(st_mode=(S_IFREG|0444), st_size=len(data), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=1)
            
    def open(self, path, flags):
        if (flags & O_ACCMODE) != os.O_RDONLY:
            raise OSError(EACCES, "")
            
        return 0
        
    def readdir(self, path, fh):
        keys = self.vdb.keys(path)
        return keys
        
    def read(self, path, size, offset, fh):
        data = self.vdb.read(path)
        
        if offset+size > len(data):
            size = len(data) - offset

        return data[offset:offset+size]

if __name__ == "__main__":
    if len(argv) != 2:
        print "usage: %s <mountpoint>" % argv[0]
        exit(1)
    fuse = FUSE(VertexDbFs(), argv[1], foreground=True)