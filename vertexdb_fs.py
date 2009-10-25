# FUSE interface for vertexdb
# by Hasan Veldstra

from errno import ENOENT, EACCES
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time
import os
import pwd
import platform

from fuse import FUSE, Operations, LoggingMixIn

from vertexdb import VertexDb

O_ACCMODE = 3

# FIXME: ENOENT for paths that don't exist.

class VertexDbFs(LoggingMixIn, Operations):

    def __init__(self):
        self.vdb = VertexDb()
        
    def getattr(self, path, fh):
        now = time() # FIXME:
        uid = pwd.getpwuid(os.getuid()).pw_uid
        gid = pwd.getpwuid(os.getuid()).pw_gid
        if self.vdb.is_dir(path):
            try:
                size = self.vdb.size(path) + 2
            except:
                raise OSError(ENOENT, "")

            if platform.system() == "Darwin":
                st_nlink = size
            elif platform.system() == "Linux":
                st_nlink = size + 2
                
            return dict(st_mode=(S_IFDIR|0766), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=st_nlink, st_uid=uid, st_gid=gid)
        else:
            try:
                data = self.vdb.read(path)
            except:
                raise OSError(ENOENT, "")

            if data == "null":
                raise OSError(ENOENT, "")
                
            return dict(st_mode=(S_IFREG|0666), st_size=len(data), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=1, st_uid=uid, st_gid=gid)
            
    def open(self, path, flags):
        return 0
        
    def access(self, path, amode):
        return 0
        
    def truncate(self, path, length, fh=None):
        return 0

    def readdir(self, path, fh):
        keys = self.vdb.keys(path)
        return [".", ".."] + keys
        
    def read(self, path, size, offset, fh):
        data = self.vdb.read(path)
        
        if offset+size > len(data):
           size = len(data) - offset

        return data[offset:offset+size]

    def write(self, path, data, offset, fh):
        w = data.split("\n")[0]
        self.vdb.write2(path, w)
        return len(w)
    
    def mknod(self, path, mode, dev):
        self.vdb.mknod(path)
        return 0

    def create(self, path, mode):
        return self.mknod(path, mode, None)

if __name__ == "__main__":
    if len(argv) != 2:
        print "usage: %s <mountpoint>" % argv[0]
        exit(1)
    fuse = FUSE(VertexDbFs(), argv[1], foreground=True)