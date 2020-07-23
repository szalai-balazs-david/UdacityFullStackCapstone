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

    def is_result_in_list(self, result_list, result):
        for result_element in result_list:
            if result['id'] == result_element['id']:
                return True
        return False

    def test_post_results_endpoint_with_basic_level_authorization_registers_test_result(self):
        post_data = {'test_id': self.create_test(), 'time': datetime.datetime.utcnow(), 'value': 3}

        res = self.client().post('/results', json=post_data, headers=basic_auth_header(True))
        data = json.loads(res.data)
        result = self.check_if_operation_was_successful_and_get_payload(data)

        res = self.client().get('/results', headers=basic_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertTrue(self.is_result_in_list(message['data'], result))

    def test_post_results_endpoint_with_advanced_level_authorization_registers_new_result(self):
        post_data = {'test_id': self.create_test(), 'time': datetime.datetime.utcnow(), 'value': 3}

        res = self.client().post('/results', json=post_data, headers=advanced_auth_header(True))
        data = json.loads(res.data)
        result = self.check_if_operation_was_successful_and_get_payload(data)

        res = self.client().get('/results', headers=advanced_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertTrue(self.is_result_in_list(message['data'], result))

    def test_post_results_endpoint_with_unregistered_test_id_throws_404(self):
        post_data = {'test_id': 1, 'time': datetime.datetime.utcnow(), 'value': 3}

        res = self.client().post('/results', json=post_data, headers=basic_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_post_results_endpoint_with_no_test_id_throws_422(self):
        post_data = {'time': datetime.datetime.utcnow(), 'value': 3}

        res = self.client().post('/results', json=post_data, headers=basic_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_post_results_endpoint_with_no_time_throws_422(self):
        post_data = {'test_id': 1, 'value': 3}

        res = self.client().post('/results', json=post_data, headers=basic_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_post_results_endpoint_with_no_value_throws_422(self):
        post_data = {'test_id': 1, 'time': datetime.datetime.utcnow()}

        res = self.client().post('/results', json=post_data, headers=basic_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_patch_profile_endpoint_with_no_authorization_returns_401(self):
        res = self.client().post('/results')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 401)
