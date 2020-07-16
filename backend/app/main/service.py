from app.main import db
from app.main.models import TestResult, Test, User
from app.main.util import get_response
from flask import abort, jsonify


def get_user_details(user_id):
    abort(404)


def update_user(id, name):
    abort(404)


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


def delete_result(user_id, id):
    abort(404)