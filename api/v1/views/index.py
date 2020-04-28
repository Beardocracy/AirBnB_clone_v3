#!/usr/bin/python3
""" Blueprint description for index """

from api.v1.views import app_views
from flask import Flask


@app_views.route('/api/v1/status', strict_slashes=False)
def status():
    """ Returns status message """
    return {"status": "OK"}
