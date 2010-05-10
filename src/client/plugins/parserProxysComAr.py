
import re
import urllib2
import time
import threading
from Proxy import Proxy

proxy_pattern = re.compile("<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\n\s*<td>(\d{1,5})</td>")
page_request_base = "http://www.proxys.com.ar/index.php?act=list&page=%i"
user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4"
headers = { 'User-Agent' : user_agent }

class parserProxysComAr():
    
    def __init__(self, proxy_checker):
        self._proxy_checker = proxy_checker
    
    def retrieve_page(self, number):
        try:
            print "Retrieving page #" + str(number) + " ..."
            page = urllib2.urlopen(urllib2.Request(page_request_base % number, headers=headers))
            print "Finished retrieving page #" + str(number)
            return page.read()
        except urllib2.HTTPError, e:
            return None
        
    def parse_page(self, page):
        tuples = list(proxyPattern.findall(page))
        proxies = []
        for tup in tuples:
            proxies.append(Proxy(ip=tup[0], port=int(tup[1])))
        return proxies
    
    def start(self):
        i = 1
        page = self.retrievePage(i)
        proxyList = self.parse_page(page)
        threads = []
        while proxyList:
            threads.append(threading.Thread(target=self._proxy_checker.check_proxies, args=[proxyList]))
            threads[-1].start()
            i += 1
            page = self.retrievePage(i)
            proxyList = self.parse_page(page)
        for thread in threads:
            thread.join()
        print "All work done"

