import json

from app.test.base_test_class import BaseTestClass, basic_auth_header, advanced_auth_header


class GetTestsTestCase(BaseTestClass):

    def test_get_results_endpoint_with_basic_level_authorization_returns_results_of_user(self):
        res = self.client().get('/results', headers=basic_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertTrue(len(message['data']) == 0)

    def test_get_results_endpoint_does_not_returns_results_of_other_users(self):
        self.add_data_to_database([
            {'test': 1, 'user': 1, 'data': 10},
            {'test': 2, 'user': 2, 'data': 10}])
        res = self.client().get('/results', headers=basic_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertTrue(len(message['data']) == 0)

    def test_get_results_endpoint_with_advanced_level_authorization_returns_results_of_user(self):
        res = self.client().get('/results', headers=advanced_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertTrue(len(message['data']) == 0)

    def test_get_results_endpoint_with_no_authorization_returns_401(self):
        res = self.client().get('/results')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 401)
