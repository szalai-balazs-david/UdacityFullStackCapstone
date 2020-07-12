from flask import request, abort, Blueprint

from app.main.util import get_response, AuthError, requires_auth
from app.main.service import *


app = Blueprint('default', __name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


@app.route('/doctors', methods=['POST'])
@requires_auth('post:doctors')
def app_post_doctor():
    abort(404)


@app.route('/doctors', methods=['GET'])
@requires_auth('get:doctors')
def app_get_doctors():
    abort(404)


@app.route('/doctors/<id>', methods=['GET'])
@requires_auth('get:doctor_details')
def app_get_doctor(id):
    abort(404)


@app.route('/doctors/<id>', methods=['PATCH'])
@requires_auth('patch:doctors')
def app_update_doctor(id):
    abort(404)


@app.route('/doctors/<id>', methods=['DELETE'])
@requires_auth('delete:doctors')
def app_delete_doctor():
    abort(404)


@app.route('/users', methods=['POST'])
@requires_auth('post:users')
def app_post_user():
    abort(404)


@app.route('/users', methods=['GET'])
@requires_auth('get:users')
def app_get_users():
    abort(404)


@app.route('/users/<id>', methods=['GET'])
@requires_auth('get:user_details')
def app_get_user(id):
    abort(404)


@app.route('/users/<id>', methods=['PATCH'])
@requires_auth('patch:users')
def app_update_user(id):
    abort(404)


@app.route('/users/<id>', methods=['DELETE'])
@requires_auth('delete:users')
def app_delete_user():
    abort(404)


@app.route('/tests', methods=['POST'])
@requires_auth('post:tests')
def app_post_tests():
    abort(404)


@app.route('/tests', methods=['GET'])
@requires_auth('get:tests')
def app_get_tests():
    abort(404)


@app.route('/results', methods=['POST'])
@requires_auth('post:results')
def app_post_results():
    abort(404)


@app.route('/results', methods=['GET'])
@requires_auth('get:results')
def app_get_results():
    abort(404)


@app.route('/results/<id>', methods=['PATCH'])
@requires_auth('patch:results')
def app_update_results(id):
    abort(404)


@app.route('/results/<id>', methods=['DELETE'])
@requires_auth('delete:results')
def app_delete_results(id):
    abort(404)


@app.errorhandler(404)
def not_found(error):
    return get_response("Not found: " + error.description, False, 404), 404


@app.errorhandler(422)
def unprocessable(error):
    return get_response("Unprocessable: " + error.description, False, 422), 422


@app.errorhandler(501)
def not_implemented(error):
    return get_response("Not Implemented: " + error.description, False, 501), 501


@app.errorhandler(AuthError)
def not_found(error):
    return get_response(error.error['description'], False, error.status_code), error.status_code
