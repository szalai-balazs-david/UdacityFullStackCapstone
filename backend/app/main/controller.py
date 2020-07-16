from flask import request, abort, Blueprint

from app.main.util import get_response, AuthError, requires_auth, get_user_id
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
    data = request.json
    if 'name' not in data:
        abort(422)
    return register_doctor(data['name'])


@app.route('/doctors', methods=['GET'])
@requires_auth('get:doctors')
def app_get_doctors():
    doctor_id = request.args.get('id', -1, type=int)
    if doctor_id == -1:
        return get_doctors()
    return get_doctor_details(doctor_id)


@app.route('/doctors/<doctor_id>', methods=['PATCH'])
@requires_auth('patch:doctors')
def app_update_doctor(doctor_id):
    data = request.json
    if 'name' not in data:
        abort(422)
    return update_doctor(doctor_id, data['name'])


@app.route('/doctors/<doctor_id>', methods=['DELETE'])
@requires_auth('delete:doctors')
def app_delete_doctor(doctor_id):
    return delete_doctor(doctor_id)


@app.route('/users', methods=['POST'])
@requires_auth('post:users')
def app_post_user():
    data = request.json
    if 'name' not in data:
        abort(422)
    if 'email' not in data:
        abort(422)
    if 'phone' not in data:
        abort(422)
    return create_user(data['name'], data['email'], data['phone'])


@app.route('/users', methods=['GET'])
@requires_auth('get:users')
def app_get_users():
    user_id = request.args.get('id', -1, type=int)
    if user_id == -1:
        return get_users()
    return get_user_details(user_id)


@app.route('/users/<id>', methods=['PATCH'])
@requires_auth('patch:users')
def app_update_user(user_id):
    data = request.json
    if 'name' not in data and 'email' not in data and 'phone' not in data:
        abort(422)
    name = data['name'] if 'name' in data else ''
    email = data['email'] if 'email' in data else ''
    phone = data['phone'] if 'phone' in data else ''
    return update_user(user_id, name, email, phone)


@app.route('/users/<user_id>', methods=['DELETE'])
@requires_auth('delete:users')
def app_delete_user(user_id):
    return delete_user(user_id)


@app.route('/tests', methods=['POST'])
@requires_auth('post:tests')
def app_post_tests():
    data = request.json
    if 'name' not in data:
        abort(422)
    return create_test(data['name'])


@app.route('/tests', methods=['GET'])
@requires_auth('get:tests')
def app_get_tests():
    return get_tests()


@app.route('/results', methods=['POST'])
@requires_auth('post:results')
def app_post_results():
    data = request.json
    if 'user_id' not in data:
        abort(422)
    if 'test_id' not in data:
        abort(422)
    if 'time' not in data:
        abort(422)
    if 'value' not in data:
        abort(422)
    return register_test_result(data['user_id'], data['test_id'], data['time'], data['value'])


@app.route('/results', methods=['GET'])
@requires_auth('get:results')
def app_get_results():
    user_id = request.args.get('id', -1, type=int)
    if user_id == -1:
        abort(422)
    test_id = request.args.get('id', -1, type=int)
    return get_test_results(user_id, test_id)


@app.route('/results/<result_id>', methods=['PATCH'])
@requires_auth('patch:results')
def app_update_results(result_id):
    data = request.json
    if 'time' not in data and 'value' not in data:
        abort(422)
    time = data['time'] if 'time' in data else ''
    value = data['value'] if 'value' in data else ''
    return update_test_result(result_id, time, value)


@app.route('/results/<result_id>', methods=['DELETE'])
@requires_auth('delete:results')
def app_delete_results(result_id):
    return delete_result(result_id)


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
