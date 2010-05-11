#!/usr/bin/env python

import sys
import BaseHTTPServer

base_response = """
        <div>
        %s
        </div>"""

class ProxyCheckerRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_GET(self):
        response_dict = {}
        response_dict['client_host_address'] = self.client_address[0]
        response_dict['client_host_port'] = self.client_address[1]
        for item in self.headers.dict.keys():
            response_dict[item] = self.headers.dict[item]
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers(  )
        string_response_dict = ""
        for item in response_dict.keys():
            string_response_dict += str(item) + " :-:-: " + str(response_dict[item]) + "\n"
        self.wfile.write(base_response % (string_response_dict,))
        return
    
    do_POST = do_GET


if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print "Bad Usage"
        exit(1)
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    
    server = BaseHTTPServer.HTTPServer((ip, port), ProxyCheckerRequestHandler)
    server.serve_forever()
