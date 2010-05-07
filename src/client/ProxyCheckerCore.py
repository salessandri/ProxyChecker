
import threading
import urllib2
import re
from xml.dom.minidom import parseString
from datetime import datetime
from Proxy import Proxy

ip_re = re.compile('((\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5])\.(\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5])\.(\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5])\.(\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5]))')

headers = { 'User-Agent' : "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4" }

ping_pages = ['http://www.google.com', 'http://www.astalavista.box.sk']

white_list_headers = set(['HTTP_X_FORWARD', 'HTTP_FORWARDED', 'HTTP_CLIENT_IP',
                          'HTTP_FORWARDED_FOR_IP', 'HTTP_X_FORWARDED','HTTP_X_FORWARDED_FOR',
                          'HTTP_FORWARDED_FOR','VIA','FORWARDED','FORWARDED_FOR_IP',
                          'HTTP_PROXY_CONNECTION','CLIENT_IP', 'FORWARDED_FOR', 'X_FORWARDED',
                          'X_FORWARDED_FOR', 'HTTP_VIA'])

brown_list_headers = set(['MAX-FORWARDS'])

class ProxyCheckerCore(Object):
    
    
    def __init__(self, db, server_url, timeout=15, max_responsivness=15000):
        self._db = db
        self._server_url = server_url
        self._timeout = timeout
        self._max_responsiveness = max_responsivness
    
    def check_proxies(self, proxy_list):
        self._total = len(proxy_list)
        self._running_semaphore = threading.Semaphore(value=0)
        for ip, port in proxy_list:
            th = threading.Thread(target=self._check_proxy,
                                  kwargs={
                                    'ip':ip,
                                    'port':port,
                                    'total':self._total,
                                    'semaphore':self._running_semaphore,
                                    })
            th.start()
        
        self._running_semaphore.acquire()
        print "Checking all the proxies is finished!"
    
    
    def _check_proxy(self, ip, port, total=None, semaphore=None):
        
        proxy = Proxy(ip, port)
        self._evaluate_responsiveness(proxy)
        if proxy.responsiveness < self._max_responsiveness:
            self._evaluate_transparency(proxy)
        
        
    
    def _evaluate_responsiveness(self, proxy):
        time_amount = 0
        for webpage in ping_pages:
            start = datetime.now()
            try:
                proxy.open(webpage, headers=headers, timeout=self._timeout)
                stop = datetime.now()
                delta = stop - start
                time_amount += delta.seconds * 1000 + delta.microseconds / 1000
            except urllib2.URLError, e:
                time_amount += (self._timeout + 5) * 1000
        time_amount /= len(ping_pages)
        proxy.responsiveness = timeAmount
    
    def _evaluate_transparency(self, proxy):
        
        ip_chicken = urllib2.urlopen('http://www.ipchicken.com/').read()
        my_ip = ip_re.search(ip_chicken).groups()[0]
        
        server_reply = proxy.open(self._server_url, headers=headers, timeout=self._timeout)
        server_reply = server_reply.read()
        
        xml_doc = parseString(server_reply)
        div = xml_doc.getElementsByTagName('div')[0]
        div_content = div.childNodes[0].nodeValue
        dict_headers = {}
        for line in div_content.strip().split('\n'):
            key, value = line.strip().split(' :-:-: ')
            dict_headers[key.strip().upper()] = value.strip()
        
        if dict_headers['CLIENT_HOST_ADDRESS'] == my_ip:
            proxy.transparency = 10
            return
        
        if len(brown_list_headers.intersection(set(dict_headers.keys()))) > 0:
            proxy.transparency = 5
            return
        
        proxy.transparency = 0
        return
