from flask_sqlalchemy import SQLAlchemy
from config import app
from environment import config

db = SQLAlchemy(app)

# http://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# TODO: Log DB queries to logger at DEBUG level
