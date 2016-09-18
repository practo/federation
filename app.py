import sys
import getopt
from app.__init__ import app


def command_help():
    print 'Usage: app.py [options]\n'
    print 'Options:'
    print '\t-h, --host    Host binding IP[0.0.0.0]'
    print '\t-p, --port    Port[8000]'
    print '\t-h, --help    Help'
    sys.exit(1)


if __name__ == '__main__':
    options, remainder = getopt.getopt(sys.argv[1:],
                                       'h:p:h', ['host=', 'port=', 'help'])
    host = '0.0.0.0'
    port = 8000
    for o, p in options:
        if o in ['-h', '--host']:
            host = p
        elif o in ['-p', '--port']:
            port = int(p)
        else:
            command_help()

    app.run(host=host, port=port)
