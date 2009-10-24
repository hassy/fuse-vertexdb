import urllib2
from urllib2 import urlopen
import simplejson as json

class VertexDb:
    
    def __init__(self, host="http://localhost:8080"):
        self.host = host
    
    def __str__(self):
        return "vertexdb at %s" % self.host
    
    def write(self, path, key, val):
        return urlopen("%s%s%s%s" % (self.host, path, "?action=write&key=", key), val).read()
        
    def read(self, path, key):
        return urlopen("%s%s%s%s" % (self.host, path, "?action=read&key=", key)).read()
        
    def mkdir(self, path):
      return urlopen("%s%s%s" % (self.host, path, "?action=mkdir")).read()

    def size(self, path):
        return urlopen("%s%s%s" % (self.host, path, "?action=size")).read()
    
    def pairs(self, path):
        return urlopen("%s%s%s" % (self.host, path, "?action=select&op=pairs")).read()
    
    def keys(self, path):
        return urlopen("%s%s%s" % (self.host, path, "?action=select&op=keys")).read()
    
    def stat(self, path):
        print "Not supported in vertexdb yet."
        return urlopen("%s%s%s" % (self.host, path, "?action=stat")).read()
        
    def is_dir(self, path):
        if path == "/":
            return True
            
        # FIXME: Returns False on empty directories. (Need stat in vertexdb.)
        # FIXME: is_dir("/test/k/") returns None when /test/k is a file.
        
        comps = [c for c in path.split("/") if c != ""]
        if len(comps) == 1:
            parent = "/"
            last = comps[0]
        else:
            parent = "/" + "/".join(comps[0:-1]) + "/"
            last = path.split("/")[-1]
        
        pairs_json = json.loads(self.pairs(parent))
        
        for e in pairs_json:
            if e[0] == last:
                if e[1] == {}:
                    return False
                else:
                    return True

vdb = VertexDb("http://localhost:8080")
print "size: ", vdb.size("/")
vdb.mkdir("/test/")
vdb.write("/test/", "akey", "avalue")
print "read: ", vdb.read("/test/", "akey")
print "keys: ", vdb.keys("/")
print "pairs: ", vdb.pairs("/")
print "is_dir: ", vdb.is_dir("/test/")

# print vdb.stat("/test/")

# Implement protocols so that nodes can be used as dictionaries etc?
# Look at fs APIs.