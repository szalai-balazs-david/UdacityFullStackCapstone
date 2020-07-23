import json

from app.test.base_test_class import BaseTestClass, basic_auth_header, advanced_auth_header


class GetTestsTestCase(BaseTestClass):

    def test_get_users_endpoint_with_basic_level_authorization_throws_403(self):
        res = self.client().get('/users', headers=basic_auth_header())
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 403)

    def test_get_users_endpoint_with_advanced_level_authorization_returns_list_of_users(self):
        self.add_data_to_database([
            {'test': 1, 'user': 1, 'data': 10},
            {'test': 2, 'user': 2, 'data': 10}])

        res = self.client().get('/users', headers=advanced_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        
        self.assertTrue(len(message) == 3)

    def test_get_users_endpoint_with_no_authorization_returns_401(self):
        res = self.client().get('/users')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 401)
