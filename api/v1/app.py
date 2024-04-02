#!/usr/bin/python3
"""
The Base application file
"""

from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_str(obj):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def handle_err_404(exception):
    """customized error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone - RESTful API',
    'uiversion': 3}

Swagger(app)


if __name__ == "__main__":

    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
