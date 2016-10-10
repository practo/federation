from app import app
import logging

app.logger.setLevel(logging.INFO)
app.logger.addHandler(logging.StreamHandler())
