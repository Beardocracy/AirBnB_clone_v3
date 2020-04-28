#!/usr/bin/python3
""" This starts the API """

from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, Blueprint, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def end_session(response_or_exc):
    """ Ends the current DB session """
    storage.close()

if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if not getenv('HBNB_API_HOST'):
        HBNB_API_HOST = '0.0.0.0'
    if not getenv('HBNB_API_PORT'):
        HBNB_API_PORT = 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
