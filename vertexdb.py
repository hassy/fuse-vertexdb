import urllib2
from urllib2 import urlopen
import simplejson as json
import os.path

class VertexDb:
    
    def __init__(self, host="http://localhost:8080"):
        self.host = host
    
    def __str__(self):
        return "vertexdb at %s" % self.host
    
    def write(self, path, key, val):
        return urlopen("%s%s%s%s" % (self.host, path, "?action=write&key=", key), val).read()
        
    def read(self, path, key=None):
        # If key is not given, use the last component of path as key.
        if key is not None:
            return urlopen("%s%s%s%s" % (self.host, path, "?action=read&key=", key)).read()
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
    
    def is_dir(self, path):
        # FIXME: Returns False on empty directories. (Need stat in vertexdb.)
        # FIXME: is_dir("/test/k/") returns None when /test/k is a file.

        if path == "/":
            return True
        
        [parent, last] = split_path(path)
        
        pairs_json = self.pairs(parent)
        
        for e in pairs_json:
            if e[0] == last:
                if e[1] == {}:
                    return False
                else:
                    return True

if __name__ == "main":
    vdb = VertexDb("http://localhost:8080")
    print "size: ", vdb.size("/")
    vdb.mkdir("/test/")
    vdb.write("/test/", "akey", "avalue")
    print "read: ", vdb.read("/test/", "akey")
    print "keys: ", vdb.keys("/")
    print "pairs: ", vdb.pairs("/")
    print "is_dir: ", vdb.is_dir("/test/")
    print "read: ", vdb.read("/test/akey")

# print vdb.stat("/test/")

# Implement protocols so that nodes can be used as dictionaries etc?
# Look at fs APIs.