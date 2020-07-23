import json

from app.test.base_test_class import BaseTestClass, basic_auth_header, advanced_auth_header


class GetTestsTestCase(BaseTestClass):

    def test_get_tests_endpoint_with_basic_level_authorization_returns_list_of_tests(self):
        self.add_data_to_database([
            {'test': 1, 'user': 1, 'data': 10},
            {'test': 2, 'user': 2, 'data': 10}])
        res = self.client().get('/tests', headers=basic_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertTrue(len(message) == 2)
        test_names = []
        for test in message:
            test_names.append(test['name'])
        self.assertTrue('Test1' in test_names)
        self.assertTrue('Test2' in test_names)

    def test_get_tests_endpoint_with_advanced_level_authorization_returns_list_of_tests(self):
        self.add_data_to_database([
            {'test': 1, 'user': 1, 'data': 10},
            {'test': 2, 'user': 2, 'data': 10}])
        res = self.client().get('/tests', headers=advanced_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertTrue(len(message) == 2)
        test_names = []
        for test in message:
            test_names.append(test['name'])
        self.assertTrue('Test1' in test_names)
        self.assertTrue('Test2' in test_names)

    def test_get_tests_endpoint_with_no_authorization_returns_401(self):
        self.add_data_to_database([
            {'test': 1, 'user': 1, 'data': 10},
            {'test': 2, 'user': 2, 'data': 10}])
        res = self.client().get('/tests')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 401)
