#!/usr/bin/env python

import sys
from ProxyCheckerDB import ProxyCheckerDB

def __parse_args(*args):
    
    where_clause = []
    sort_clause = None
    limit_clause = None
    db = None
    
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
        else:
            db = arg
    
    return db, where_clause, sort_clause, limit_clause

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
        return sys.argv[0] + """ show [options] <dabatase_name>
        
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
    
    db, where_clause, sort_clause, limit_clause = __parse_args(*args)
    
    if db == None:
        print "No database selected!"
        exit(1)
    
    proxy_checker = ProxyCheckerDB(db)
    
    proxy_list = proxy_checker.get_proxies(where_clause=where_clause,
                                           sort_clause=sort_clause,
                                           limit_clause=limit_clause)
    
    __printResults(proxy_list)
    exit(0)

def update(*args):
    def help():
        return sys.argv[0] + """ update [options] <dabatase_name>
        
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
    
    db, where_clause, sort_clause, limit_clause = __parse_args(*args)
    
    if db == None:
        print "No database selected!"
        exit(1)
    
    proxy_checker = ProxyCheckerDB(db)
    
    proxy_list = proxy_checker.get_proxies(where_clause=where_clause,
                                           sort_clause=sort_clause,
                                           limit_clause=limit_clause)
    
    print "Starting checking..."
    proxy_checker.check_proxies(proxy_list)
    print "Checking Done"
    exit(0)
    

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
    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv:
        print help()
        exit(0)
    globals.__getattr__(sys.argv[1], sys.argv[2:])
    
    