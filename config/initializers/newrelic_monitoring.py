class NewrelicMonitoring():
    def __init__(self, app):
        config = app.config
        ENV = config.get('ENVIORNMENT')

        if config.get('ENABLE_NEWRELIC_MONITORING', False):
            newrelic_ini = config.get('NEWRELIC_INI_PATH', False)
            if(newrelic_ini):
                from newrelic import agent as newrelic_agent

                newrelic_agent.initialize(newrelic_ini, ENV.lower())
                app.wsgi_app = newrelic_agent.\
                    WSGIApplicationWrapper(app.wsgi_app)
