import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app.main.models import TestResult, Test, User
from app.main import create_app
from app.main import db
import datetime
import os


def basic_auth_header(add_content_type=False):
    if add_content_type:
        return {'Authorization': 'Bearer ' + os.getenv('BASIC_TOKEN'),
                'Content-Type': 'application/json'}
    return {'Authorization': 'Bearer ' + os.getenv('BASIC_TOKEN')}


def advanced_auth_header(add_content_type=False):
    if add_content_type:
        return {'Authorization': 'Bearer ' + os.getenv('ADVANCED_TOKEN'),
                'Content-Type': 'application/json'}
    return {'Authorization': 'Bearer ' + os.getenv('ADVANCED_TOKEN')}


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            db.create_all()
            db.session.commit()

            self.db.session.query(TestResult).delete()
            self.db.session.query(Test).delete()
            self.db.session.query(User).delete()
            self.db.session.commit()

    def tearDown(self):
        pass

    def check_if_operation_was_successful_and_get_payload(self, data):
        self.assertTrue(data['success'])
        self.assertEqual(0, data['error'])
        return data['message']

    def check_if_operation_failed_with_error_code(self, data, expected_error_code):
        self.assertFalse(data['success'])
        self.assertEqual(expected_error_code, data['error'])

    def add_data_to_database(self, data):
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            for datapoint in data:
                test = Test()
                test.name = "Test" + str(datapoint['test'])
                self.db.session.add(test)
                user = User()
                user.auth0_id = "User" + str(datapoint['user'])
                user.name = "User" + str(datapoint['user'])
                user.email = "User" + str(datapoint['user'])
                self.db.session.add(user)
                self.db.session.commit()
                for j in range(datapoint['data']):
                    result = TestResult()
                    result.test_id = test.id
                    result.user_id = user.id
                    result.value = j
                    result.time = datetime.datetime.utcnow()
                    self.db.session.add(result)
                self.db.session.commit()
