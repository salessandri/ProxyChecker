#!/usr/bin/env python

from ProxyCheckerCore import ProxyCheckerCore
from Proxy import Proxy

class ProxyCheckerDB(object):
    
    def __init__(self, db, server_url, timeout=15, max_responsivness=15000):
        self._db = db
        self._server_url = server_url
        self._timeout = timeout
        self._max_responsivness = max_responsivness
    
    def check_proxies(self, proxy_list):
        core = ProxyCheckerCore(self._server_url, self._timeout, self._max_responsivness)
        proxies = core.check_proxies(proxy_list)
        
        con = sqlite.connect(self._db)
        cursor = con.cursor()
        for proxy in proxies:
            query = """SELECT ip, port, transparency, responsiveness
                        FROM proxy
                        WHERE ip = '%s' AND port = %d """ % (proxy.ip, proxy.port)
            resp = cursor.execute(query)
            if resp:
                query = """UPDATE proxy
                            SET transparency = %s,
                            responsiveness = %s,
                            last_checked = '%s'
                            WHERE ip = '%s' AND
                            port = %d""" % (proxy.transparency, proxy.responsiveness, str(datetime.now()), proxy.ip, proxy.port)
            else:
                query = """INSERT INTO proxy (ip, port, last_checked, transparency, responsiveness)
                                    VALUES ('%s', %s, '%s', %s, %s) """ % (proxy.ip, proxy.port, proxy.last_checked, proxy.transparency, proxy.responsiveness)
            cursor.execute(query)
        con.commit()
        con.close()
    
    def get_proxies(self, **kwargs):
        
        where_clause = kwargs.get('where_clause', None)
        sort_clause = kwargs.get('sort_clause', None)
        limit_clause = kwargs.get('limit_clause', None)
        
        query = "SELECT ip, port, responsiveness, transparency, last_checked FROM proxy "
        if where_clause:
            query += "WHERE " + ' AND '.join(where_clause) + ' '
        if sort_clause:
            query += "ORDER BY %s " % (sort_clause,)
        if limit_clause:
            query += "LIMIT %d" % (limit_clause,)
        
        con = sqlite.connect(self._db)
        cursor = con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        proxy_list = []
        for proxy in results:
            proxy_list.append(Proxy(proxy[0], proxy[1], last_checked=proxy[2], transparency=proxy[3], responsiveness=proxy[4]))
        
        return proxy_list
    
    def install_db(self):
        con = sqlite.connect(self._db)
        cur = con.cursor()
        cur.execute("""CREATE TABLE proxy (id INTEGER PRIMARY KEY, ip VARCHAR[20], port INTEGER, responsiveness INTEGER, transparency INTEGER, last_checked VARCHAR[120])""")
        con.commit()
        con.close()
        return
    
    