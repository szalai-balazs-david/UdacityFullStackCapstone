from flask import request, abort, Blueprint

from app.main.util import get_response, AuthError, requires_auth, get_user_id
from app.main.service import *


app = Blueprint('default', __name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


@app.route('/profile', methods=['GET'])
@requires_auth('get:profile')
def app_get_profile():
    user_id = get_user_id()
    return get_profile(user_id)


@app.route('/profile', methods=['PATCH'])
@requires_auth('patch:profile')
def app_update_profile():
    user_id = get_user_id()
    data = request.json
    if 'name' not in data:
        abort(422)
    return update_profile(user_id, data['name'])


@app.route('/tests', methods=['GET'])
@requires_auth('get:tests')
def app_get_tests():
    return get_tests()


@app.route('/tests', methods=['POST'])
@requires_auth('post:tests')
def app_post_tests():
    data = request.json
    if 'name' not in data:
        abort(422)
    return create_test(data['name'])


@app.route('/results', methods=['GET'])
@requires_auth('get:results')
def app_get_results():
    user_id = get_user_id()
    #ToDo: add time range?
    test_id = request.args.get('id', -1, type=int)
    return get_test_results(user_id, test_id)


@app.route('/results', methods=['POST'])
@requires_auth('post:results')
def app_post_results():
    user_id = get_user_id()
    data = request.json
    if 'test_id' not in data:
        abort(422)
    if 'time' not in data:
        abort(422)
    if 'value' not in data:
        abort(422)
    return register_test_result(user_id, data['test_id'], data['time'], data['value'])


@app.route('/results/<result_id>', methods=['PATCH'])
@requires_auth('patch:results')
def app_update_results(result_id):
    user_id = get_user_id()
    data = request.json
    if 'time' not in data and 'value' not in data:
        abort(422)
    time = data['time'] if 'time' in data else ''
    value = data['value'] if 'value' in data else ''
    return update_test_result(user_id, result_id, time, value)


@app.route('/results/<result_id>', methods=['DELETE'])
@requires_auth('delete:results')
def app_delete_results(result_id):
    user_id = get_user_id()
    return delete_result(user_id, result_id)


@app.route('/users', methods=['GET'])
@requires_auth('get:users')
def app_get_users():
    get_user_id()
    return get_available_users()


@app.route('/users/<user_id>/results', methods=['GET'])
@requires_auth('get:patient_results')
def app_get_user_results(user_id):
    test_id = request.args.get('test_id', -1, type=int)
    return get_test_results(user_id, test_id)


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
