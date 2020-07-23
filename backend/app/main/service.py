from app.main import db
from app.main.models import TestResult, Test, User
from app.main.util import get_response
from flask import abort, jsonify
from app.main.util import AuthError
from dateutil import parser


def user_to_short_string(user):
    ids = []
    tests = []
    for result in user.results:
        if result.test_id not in ids:
            # todo: add test name in addition to test id
            ids.append(result.test_id)
            tests.append({
                'id': result.test_id,
                'name': result.test.name
            })
    return {
        'id': user.id,
        'name': user.name if user.name is not None else "Unknown",
        'tests': tests
    }


def test_to_short_string(test):
    return {
        'id': test.id,
        'name': test.name
    }


def result_to_short_string(result):
    return {
        'id': result.id,
        'user_id': result.user_id,
        'test_id': result.test_id,
        'time': result.time,
        'value': result.value
    }


def get_profile(user_id):
    user = User.query.get(user_id)
    return get_response(user_to_short_string(user))


def update_profile(user_id, name):
    user = User.query.get(user_id)
    user.name = name
    db.session.commit()
    return get_response(user_to_short_string(user))


def create_test(name):
    test = Test.query.filter(Test.name == name).first()
    if test is None:
        new_test = Test()
        new_test.name = name
        db.session.add(new_test)
        db.session.commit()
        return get_response(test_to_short_string(new_test))
    else:
        abort(422, "Name already exists")


def get_tests():
    tests = Test.query.all()
    data = []
    for test in tests:
        data.append(test_to_short_string(test))
    return get_response(data)


def register_test_result(user_id, test_id, time, value):
    if Test.query.get(test_id) is None:
        abort(404)

    result = TestResult()
    result.user_id = user_id
    result.test_id = test_id
    result.time = parser.parse(time)
    result.value = value
    db.session.add(result)
    db.session.commit()
    return get_response(result_to_short_string(result))


def get_test_results(user_id, test_id):
    if test_id == -1:
        results = TestResult.query.filter(TestResult.user_id == user_id).all()
    else:
        results = TestResult.query.filter(TestResult.user_id == user_id).filter(TestResult.test_id == test_id).all()

    data = []
    for result in results:
        data.append(result_to_short_string(result))

    # todo: test_id and user_id are duplications...
    return get_response({
        'test_id': test_id,
        'user_id': user_id,
        'data': data
    })


def update_test_result(user_id, result_id, time, value):
    result = TestResult.query.get(result_id)
    if result is None:
        abort(404)
    if result.user_id != user_id:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Test result belongs to another user.'
        }, 403)

    if time != '':
        result.time = parser.parse(time)
    if value != '':
        result.value = value
    db.session.commit()

    return get_response(result_to_short_string(result))


def delete_result(user_id, result_id):
    result = TestResult.query.get(result_id)
    if result is None:
        abort(404)
    if result.user_id != user_id:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Test result belongs to another user.'
        }, 403)

    db.session.delete(result)
    db.session.commit()

    return get_response(result_id)


def get_available_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append(user_to_short_string(user))
    return get_response(result)
