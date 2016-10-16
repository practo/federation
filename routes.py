import urllib
from flask import url_for
from config.app import create_app

output = []
app = create_app()
app.config['SERVER_NAME'] = '<HOST_NAME>:<HOST_PORT>'

with app.app_context():
    # Router has to be imported at last as it in turns loads the application code
    from config.router import load_blueprints
    load_blueprints(app)

    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods,
                                                        url))
        output.append(line)

for line in sorted(output):
    print(line)
