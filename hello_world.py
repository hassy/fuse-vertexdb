# HelloWorld filesystem in Python. 
# Ported from the C example in: http://www.macdevcenter.com/pub/a/mac/2007/03/06/macfuse-new-frontiers-in-file-systems.html

from errno import ENOENT, EACCES
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time
import os

from fuse import FUSE, Operations, LoggingMixIn

O_ACCMODE = 3

class Hello(Operations):

    def __init__(self):
        self.file_path = "/hello.txt"
        self.file_contents = "Hello world!\n"

    def getattr(self, path, fh=None):
        """
        Returns a dictionary with keys identical to the stat C structure
        of stat(2). st_atime, st_mtime and st_ctime should be floats.
        On OSX, st_nlink should count all files inside the directory.
        On Linux, only the subdirectories are counted.
        """
        
        now = time()
        if path == "/":
            return dict(st_mode=(S_IFDIR|0755), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=3)
        elif path == self.file_path:
            return dict(st_mode=(S_IFREG|0444), st_size=len(self.file_contents), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=1)
        else:
            raise OSError(ENOENT, "")
            
    def open(self, path, flags):
        if path != self.file_path:
            raise OSError(ENOENT, "")
        
        if (flags & O_ACCMODE) != os.O_RDONLY:
            raise OSError(EACCES, "")

        return 0
        
    def readdir(self, path, fh):
        """
        Can return either a list of names, or a list of (name, attrs, offset)
        tuples. attrs is a dict as in getattr.
        """
        
        if path != "/":
            raise OSError(ENOENT, "")
            
        return [".", "..", "hello.txt"]
        
    def read(self, path, size, offset, fh):
        if path != self.file_path:
            raise OSError(EACCESS, "")
            
        if offset+size > len(self.file_contents):
            size = len(self.file_contents) - offset
            
        return self.file_contents[offset:offset+size]
            
        

if __name__ == "__main__":
    if len(argv) != 2:
        print 'usage: %s <mountpoint>' % argv[0]
        exit(1)
    fuse = FUSE(Hello(), argv[1], foreground=True)