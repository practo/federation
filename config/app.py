from flask import Flask
from environment import load_config
from db import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    load_config(app)
    db.init_app(app)

    return app
