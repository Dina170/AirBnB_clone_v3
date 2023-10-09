#!/usr/bin/python3
"""Starts a new flask application"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(_):
    """After each request remove the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def error(error):
    """Handle not found error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
