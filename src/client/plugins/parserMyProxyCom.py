
import re
import urllib2
import time
import threading
from Proxy import Proxy

proxy_pattern = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,6})<br>")
page_request_base = "http://proxies.my-proxy.com/proxy-list-%i.html"
user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4"
headers = { 'User-Agent' : user_agent }

class parserMyProxyCom():
    
    def __init__(self, proxy_checker):
        self._proxy_checker = proxy_checker
    
    def retrieve_page(self, number):
        try:
            print "Retrieving page #" + str(number) + " ..."
            page = urllib2.urlopen(urllib2.Request(page_request_base % number, headers=headers))
            print "Finished retrieving page #" + str(number)
            return page.read()
        except urllib2.HTTPError, e:
            return ''
        
    def parse_page(self, page):
        tuples = list(proxy_pattern.findall(page))
        proxies = []
        for tup in tuples:
            proxies.append(Proxy(ip=tup[0], port=int(tup[1])))
        return proxies
    
    def start(self):
        i = 1
        page = self.retrieve_page(i)
        proxy_list = self.parse_page(page)
        all_proxies = []
        while proxy_list:
            all_proxies.extend(proxy_list)
            i += 1
            page = self.retrieve_page(i)
            proxy_list = self.parse_page(page)
        self._proxy_checker.check_proxies(all_proxies)
        print "All work done"

