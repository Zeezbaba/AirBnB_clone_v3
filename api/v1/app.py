#!/usr/bin/python3
"""
The Base application file
"""

from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, make_response, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_str(obj):
    """close storage"""
    storage.close()


@app.errorhandler
def handle_err_404(exception):
    """customized error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":

    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
