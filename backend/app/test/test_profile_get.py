import json

from app.test.base_test_class import BaseTestClass, basic_auth_header, advanced_auth_header


class GetTestsTestCase(BaseTestClass):

    def test_get_profile_endpoint_with_basic_level_authorization_returns_user_info(self):
        res = self.client().get('/profile', headers=basic_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertTrue(message['name'] == 'Unknown')
        self.assertTrue(len(message['tests']) == 0)

    def test_get_profile_endpoint_with_advanced_level_authorization_returns_user_info(self):
        res = self.client().get('/profile', headers=advanced_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertTrue(message['name'] == 'Unknown')
        self.assertTrue(len(message['tests']) == 0)

    def test_get_profile_endpoint_with_no_authorization_returns_401(self):
        res = self.client().get('/profile')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 401)
