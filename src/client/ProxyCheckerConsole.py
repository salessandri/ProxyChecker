#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from ProxyCheckerDB import ProxyCheckerDB

def __parse_args(*args):
    
    where_clause = []
    sort_clause = None
    limit_clause = None
    db = None
    server_url = None
    plugin_list = []
    
    args = list(args)
    while args:
        arg = args.pop(0)
        if arg == "-ip":
            where_clause.append("ip LIKE '%s'" % ('%'+args.pop(0)+'%'))
        elif arg == "-p":
            ports = args.pop(0)
            ports = ports.split(',')
            modifier = []
            for port in ports:
                if ":" in port:
                    modifier.append("port BETWEEN %d AND %d" % (map(int, port.split(':'))))
                else:
                    modifier.append("port = %d" % (int(port),))
            where_clause.append("(" + " OR ".join(modifier) + " )")
        elif arg == '-tr':
            comp = args.pop(0)
            value = int(args.pop(0))
            if comp == 'eq':
                where_clause.append("transparency = %d" (value,))
            elif comp == 'ne':
                where_clause.append("transparency <> %d" (value,))
            elif comp == 'le':
                where_clause.append("transparency <= %d" (value,))
            elif comp == 'ge':
                where_clause.append("transparency >= %d" (value,))
        elif arg == '-re':
            comp = args.pop(0)
            value = int(args.pop(0))
            if comp == 'eq':
                where_clause.append("responsiveness = %d" (value,))
            elif comp == 'ne':
                where_clause.append("responsiveness <> %d" (value,))
            elif comp == 'le':
                where_clause.append("responsiveness <= %d" (value,))
            elif comp == 'ge':
                where_clause.append("responsiveness >= %d" (value,))
        elif arg == '-sort':
            sort_clause = args.pop(0)
        elif arg == '-limit':
            limit_clause = int(args.pop(0))
        elif arg == '-db':
            db = args.pop(0)
        elif arg == '-url':
            server_url = args.pop(0)
        elif arg == '-pl':
            plugin_list.extend(args.pop(0).split(','))
        
    
    return locals()

def install(*args):
    
    def help():
        return sys.argv[0] + " install <dabatase_name>\n\n->Creates a database to use"
    
    if "-h" in args or "--help" in args:
        print help()
        exit(0)
    db = args[0]
    proxy_checker = ProxyCheckerDB(db)
    print "Creating database..."
    proxy_checker.install_db()
    print "Creating database... DONE!"
    exit(0)
    
def show(*args):
    
    def help():
        return sys.argv[0] + """ show [options] -db <dabatase_name>
        
        Shows the different proxies stored in the database. Options are used to
        restrict the showed proxies.
        
        Options are:
            -ip <ip value or part to compare>
            -p <port single port, range like xxxx:yyyy or some ports with xxxx,yyyy.
            -tr <modifier> <value>
            -re <modifier> <value>
            -sort <ip, port, transparency, responsivness, last_checked>
            -limit <value>
        
        Modifiers are:
            eq = equals
            ne = not equals
            le = lower or equal
            ge = greater or equal
        """
    
    if "-h" in args or "--help" in args:
        print help()
        exit(0)
    
    parsed_args = __parse_args(*args)
    
    if parsed_args['db'] == None:
        print "No database selected!"
        exit(1)
    
    proxy_checker = ProxyCheckerDB(parsed_args['db'])
    
    proxy_list = proxy_checker.get_proxies(where_clause=parsed_args['where_clause'],
                                           sort_clause=parsed_args['sort_clause'],
                                           limit_clause=parsed_args['limit_clause'])
    
    __printResults(proxy_list)
    exit(0)

def update(*args):
    def help():
        return sys.argv[0] + """ update [options] -db <dabatase_name> -url <server_url>
        
        Updates the different proxies stored in the database. Options are used to
        restrict the proxies to update.
        
        Options are:
            -ip <ip value or part to compare>
            -p <port single port, range like xxxx:yyyy or some ports with xxxx,yyyy.
            -tr <modifier> <value>
            -re <modifier> <value>
            -sort <ip, port, transparency, responsivness, last_checked>
            -limit <value>
        
        Modifiers are:
            eq = equals
            ne = not equals
            le = lower or equal
            ge = greater or equal
        """
    
    if "-h" in args or "--help" in args:
        print help()
        exit(0)
    
    pased_args = __parse_args(*args)
    
    if parsed_args['db'] == None:
        print "No database selected!"
        exit(1)
    
    if parsed_args['server_url'] == None:
        print "No server's url selected!"
        exit(1)
    
    proxy_checker = ProxyCheckerDB(parsed_args['db'], parsed_args['server_url'])
    
    proxy_list = proxy_checker.get_proxies(where_clause=parsed_args['where_clause'],
                                           sort_clause=parsed_args['sort_clause'],
                                           limit_clause=parsed_args['limit_clause'])
    
    print "Starting checking..."
    proxy_checker.check_proxies(proxy_list)
    print "Checking Done"
    exit(0)

def run(*args):
    
    def help():
        return sys.argv[0] + """ run -pl <plugin_name>,... -db <dabatase_name> -url <server_url>
        
        """
    
    if "-h" in args or "--help" in args:
        print help()
        exit(0)
    
    parsed_args = __parse_args(*args)
    
    if parsed_args['db'] == None:
        print "No database selected!"
        exit(1)
    
    if parsed_args['server_url'] == None:
        print "No server's url selected!"
        exit(1)
        
    proxy_checker = ProxyCheckerDB(parsed_args['db'], parsed_args['server_url'])
    
    for plugin_name in parsed_args['plugin_list']:
        try:
            print 'plugins.' + plugin_name
            module = __import__('plugins.' + plugin_name)
        except Exception,e:
            print e
            exit(2)
        print module
        plugin = getattr(module, plugin_name)(proxy_checker)
        plugin.start()
    

def __printResults(proxies):
        print "=" * 73
        print "|      Proxy       |  Port  |  Resp. | Tra.|       Last Checked         |"
        for proxy in proxies:
            print "| %16s | %5d  | %6d | %3d | %16s |" % (proxy.ip,
                                                          proxy.port,
                                                          proxy.responsivness,
                                                          proxy.transparency,
                                                          proxy.last_checked)
        print "=" * 73

def help():
        return sys.argv[0] + " action [params]"

if __name__ == '__main__':
    if len(sys.argv) < 2 or '-h' == sys.argv[1] or '--help' == sys.argv[1]:
        print help()
        exit(0)
    globals().get(sys.argv[1])(*sys.argv[2:])
    
    