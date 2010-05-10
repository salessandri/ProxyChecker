
import urllib2


class Proxy(object):
    
    def __init__(self, ip, port, https=None, transparency=None, responsiveness=None, last_checked=None):
        self.ip = ip
        self.port = port
        self.https = https
        self.transparency = transparency
        self.responsiveness = responsiveness
        self.last_checked = last_checked
    
    def __str__(self):
        return str(self.ip) + ":" + str(self.port)
    
    def open(self, url, headers={}, timeout=None):
        handler = urllib2.ProxyHandler({'http': '%s:%s' % (self.ip, self.port,)})
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(webpage, headers=headers)
        page = opener.open(req, timeout)
        return page
        
    
    
