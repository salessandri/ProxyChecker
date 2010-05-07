
import urllib2


class Proxy(Object):
    
    self.ip = None
    self.port = None
    self.https = None
    self.transparency = None
    self.responsiveness = None
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
    def __str__(self):
        return str(self.ip) + ":" + str(self.port)
    
    def open(self, url, headers={}, timeout=None):
        handler = urllib2.ProxyHandler({'http': '%s:%s' % (self.ip, self.port,)})
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(webpage, headers=headers)
        page = opener.open(req, timeout)
        return page
        
    
    
