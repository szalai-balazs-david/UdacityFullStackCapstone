import json

from app.test.base_test_class import BaseTestClass, basic_auth_header, advanced_auth_header


class GetTestsTestCase(BaseTestClass):

    def test_post_tests_endpoint_with_basic_level_authorization_returns_403(self):
        post_data = {'name': 'someName'}

        res = self.client().post('/tests', json=post_data, headers=basic_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 403)

    def test_post_tests_endpoint_with_advanced_level_authorization_registers_new_test(self):
        post_data = {'name': 'someName'}

        res = self.client().get('/tests', headers=advanced_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertEqual(len(message), 0)

        res = self.client().post('/tests', json=post_data, headers=advanced_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_was_successful_and_get_payload(data)

        res = self.client().get('/tests', headers=advanced_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertEqual(len(message), 1)
        self.assertTrue(message[0]['name'] == post_data['name'])

    def test_post_tests_endpoint_with_advanced_level_authorization_and_existing_test_name_returns_422(self):
        post_data = {'name': 'someName'}

        res = self.client().get('/tests', headers=advanced_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertEqual(len(message), 0)

        res = self.client().post('/tests', json=post_data, headers=advanced_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_was_successful_and_get_payload(data)

        res = self.client().post('/tests', json=post_data, headers=advanced_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_post_tests_endpoint_with_advanced_level_authorization_without_name_in_payload_returns_422(self):
        post_data = {}

        res = self.client().post('/tests', json=post_data, headers=advanced_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_patch_profile_endpoint_with_no_authorization_returns_401(self):
        res = self.client().post('/tests')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 401)
