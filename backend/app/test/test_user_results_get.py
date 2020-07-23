import json
import datetime

from app.test.base_test_class import BaseTestClass, basic_auth_header, advanced_auth_header


class GetTestsTestCase(BaseTestClass):

    def create_test(self):
        post_data = {'name': 'someName'}
        res = self.client().post('/tests', json=post_data, headers=advanced_auth_header(True))
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        return message['id']

    def test_get_user_results_endpoint_with_basic_level_authorization_throws_403(self):
        res = self.client().get('/users', headers=basic_auth_header())
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 403)

    def test_get_user_results_endpoint_with_advanced_level_authorization_returns_list_of_results_of_user(self):
        res = self.client().get('/profile', headers=basic_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        user_id = message['id']

        post_data = {'test_id': self.create_test(), 'time': datetime.datetime.utcnow(), 'value': 3}

        self.client().post('/results', json=post_data, headers=basic_auth_header(True))
        self.client().post('/results', json=post_data, headers=basic_auth_header(True))
        self.client().post('/results', json=post_data, headers=basic_auth_header(True))

        res = self.client().get('/users/' + str(user_id) + '/results', headers=advanced_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertTrue(len(message['data']) == 3)

    def test_get_user_results_endpoint_with_no_authorization_returns_401(self):
        res = self.client().get('/users')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 401)
