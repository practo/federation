import urllib
from flask import url_for
from app import app

output = []
app.config['SERVER_NAME'] = '<HOST_NAME>:<HOST_PORT>'

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
