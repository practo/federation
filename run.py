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
    from config.app import create_app
    from config.initializers.newrelic_monitoring import NewrelicMonitoring
    from config.initializers.errors import RequestErrorHandling

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

    app = create_app()

    RequestErrorHandling(app)
    NewrelicMonitoring(app)

    # Router has to be imported at last as it in turns loads the application code
    with app.app_context():
        from config.router import load_blueprints
        load_blueprints(app)

    app.run(host=host, port=port)
