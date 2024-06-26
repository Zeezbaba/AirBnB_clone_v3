#!/usr/bin/python3
"""
The Base application file
"""

from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, make_response, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=['0.0.0.0'])
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_str(obj):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def handle_err_404(exception):
    """customized error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":

    HOST = getenv('HBNB_API_HOST', default='0.0.0.0')
    PORT = getenv('HBNB_API_PORT', default=5000)

    app.run(host=HOST, port=int(PORT), threaded=True)
