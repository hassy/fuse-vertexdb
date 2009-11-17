# Super-simple bindings for Vertexdb.
# Hasan Veldstra <hasan@12monkeys.co.uk>
# License: same as Python.

import urllib2
from urllib2 import urlopen
try:
    import simplejson as json
except:
    import json
import os.path

class VertexDb:
    
    def __init__(self, host="http://localhost:8080"):
        self.host = host
    
    def __str__(self):
        return "vertexdb at %s" % self.host
    
    def write(self, path, key, val):
        return urlopen("%s%s%s%s%s%s" % (self.host, path, "?action=write&key=", key, "&value=", val)).read()

    def write2(self, path, val):
        return self.write(os.path.dirname(path), os.path.basename(path), val)
        
    def read(self, path, key=None):
        # If key is not given, use the last component of path as key.
        if key is not None:
            data = urlopen("%s%s%s%s" % (self.host, path, "?action=read&key=", key)).read()
            return data[1:-1]
        else:
            return self.read(os.path.dirname(path), os.path.basename(path))
        
    def mkdir(self, path):
      return urlopen("%s%s%s" % (self.host, path, "?action=mkdir")).read()

    def size(self, path):
        return int(urlopen("%s%s%s" % (self.host, path, "?action=size")).read())
    
    def pairs(self, path):
        return json.loads(urlopen("%s%s%s" % (self.host, path, "?action=select&op=pairs")).read())
    
    def keys(self, path):
        return json.loads(urlopen("%s%s%s" % (self.host, path, "?action=select&op=keys")).read())
    
    def stat(self, path):
        print "Not supported in vertexdb yet."
        return urlopen("%s%s%s" % (self.host, path, "?action=stat")).read()
    
    def mknod(self, path, key=None):
        """
        vdb.mknod("/some/path/", "_newkey")
            or
        vdb.mknod("/some/path/_newkey")
        """
        if key is not None:
            return self.write(path, key, "")
        else:
            return self.write2(path, "")
    
    def is_dir(self, path):
        return not(os.path.basename(path).startswith("_"))
