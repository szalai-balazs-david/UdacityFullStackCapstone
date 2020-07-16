from app.main import db
from app.main.models import TestResult, Test, User
from app.main.util import get_response
from flask import abort, jsonify


def user_to_short_string(user):
    tests = []
    for result in User.results:
        if result.test_id not in tests:
            # todo: add test name in addition to test id
            tests.append(result.test_id)
    return {
        'id': user.id,
        'name': user.name if user.name is not None else user.auth0_id,
        'tests': tests
    }


def get_user_details(user_id):
    user = User.query.get(user_id)
    return get_response(user_to_short_string(user))


def update_user(user_id, name):
    user = User.query.get(user_id)
    user.name = name
    db.session.commit()
    return get_user_details(user_to_short_string(user))


def create_test(name):
    abort(404)


def get_tests():
    abort(404)


def register_test_result(user_id, test_id, time, value):
    abort(404)


def get_test_results(user_id, test_id):
    abort(404)


def update_test_result(user_id, result_id, time, value):
    abort(404)


def delete_result(user_id, result_id):
    abort(404)