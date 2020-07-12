from flask import request, abort, Blueprint

from app.main.util import get_response
from app.main.service import *


app = Blueprint('default', __name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


@app.errorhandler(404)
def not_found(error):
    return get_response("Not found: " + error.description, False, 404), 404


@app.errorhandler(422)
def unprocessable(error):
    return get_response("Unprocessable: " + error.description, False, 422), 422


@app.errorhandler(501)
def not_implemented(error):
    return get_response("Not Implemented: " + error.description, False, 501), 501
