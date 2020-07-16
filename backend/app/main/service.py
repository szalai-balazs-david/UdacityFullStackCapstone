from app.main import db
from app.main.models import Doctor, TestResult, Test, User
from app.main.util import get_response
from flask import abort, jsonify


def register_doctor(name):
    abort(404)


def get_doctors():
    abort(404)


def get_doctor_details(id):
    abort(404)


def update_doctor(id, name):
    abort(404)


def delete_doctor(id):
    abort(404)


def create_user(name, email, phone):
    abort(404)


def get_users():
    abort(404)


def get_user_details(user_id):
    abort(404)


def update_user(id, name, email, phone):
    abort(404)


def delete_user(id):
    abort(404)


def create_test(name):
    abort(404)


def get_tests():
    abort(404)


def register_test_result(user_id, test_id, time, value):
    abort(404)


def get_test_results(user_id, test_id):
    abort(404)


def update_test_result(result_id, time, value):
    abort(404)


def delete_result(id):
    abort(404)