#!/usr/bin/env python

import sys

def install(*args):
    
    db = args[0]
    print "Creating database..."
    con = sqlite.connect(db)
    cur = con.cursor()
    cur.execute("""CREATE TABLE proxy (id INTEGER PRIMARY KEY, ip VARCHAR[20], port INTEGER, responsiveness INTEGER, transparency INTEGER, lastChecked VARCHAR[120])""")
    con.commit()
    con.close()
    print "Creating database... DONE!"
    


def help():
        return sys.argv[0] + " action [params]"

if __name__ == '__main__':
    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv:
        print help()
        exit(0)
    globals.__getattr__(sys.argv[1], sys.argv[2:])
    
    