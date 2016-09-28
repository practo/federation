import urllib
from flask import url_for
from app import app
from config.routes import blueprints

output = []
app.config['SERVER_NAME'] = '<HOST_NAME>:<HOST_PORT>'
for blueprint_name, blueprint_url_prefix in blueprints:
    app.register_blueprint(blueprint_name, url_prefix=blueprint_url_prefix)

with app.app_context():
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
