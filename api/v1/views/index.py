#!/usr/bin/python3
"""index view"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Get the status of api"""
    return jsonify({"status": "OK"})
