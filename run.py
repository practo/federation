def command_help():
    print('Usage: app.py [options]\n')
    print('Options:')
    print('\t-h, --host    Host binding IP[0.0.0.0]')
    print('\t-p, --port    Port[1786]')
    print('\t-h, --help    Help')
    sys.exit(1)

if __name__ == '__main__':
    import sys
    import getopt
    from config.router import blueprints
    from config.initializers.newrelic_monitoring import NewrelicMonitoring
    from config import app

    options, remainder = getopt.getopt(sys.argv[1:],
                                       'h:p:h', ['host=', 'port=', 'help'])
    host = '0.0.0.0'
    port = 1786
    for key, value in options:
        if key in ['-h', '--host']:
            host = value
        elif key in ['-p', '--port']:
            port = int(key)
        else:
            command_help()

    for blueprint_name, blueprint_url_prefix in blueprints:
        app.register_blueprint(blueprint_name, url_prefix=blueprint_url_prefix)

    NewrelicMonitoring()

    app.run(host=host, port=port)
