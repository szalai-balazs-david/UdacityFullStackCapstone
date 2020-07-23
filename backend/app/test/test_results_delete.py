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

    def test_delete_results_endpoint_with_basic_level_authorization_deletes_result(self):
        post_data = {'test_id': self.create_test(), 'time': datetime.datetime.utcnow(), 'value': 3}

        res = self.client().post('/results', json=post_data, headers=basic_auth_header(True))
        data = json.loads(res.data)
        post_result = self.check_if_operation_was_successful_and_get_payload(data)

        res = self.client().delete('/results/' + str(post_result['id']), headers=basic_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_was_successful_and_get_payload(data)

        res = self.client().get('/results', headers=basic_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertTrue(len(message['data']) == 0)

    def test_delete_results_endpoint_with_advanced_level_authorization_deletes_result(self):
        post_data = {'test_id': self.create_test(), 'time': datetime.datetime.utcnow(), 'value': 3}

        res = self.client().post('/results', json=post_data, headers=advanced_auth_header(True))
        data = json.loads(res.data)
        post_result = self.check_if_operation_was_successful_and_get_payload(data)

        res = self.client().delete('/results/' + str(post_result['id']), headers=advanced_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_was_successful_and_get_payload(data)

        res = self.client().get('/results', headers=advanced_auth_header())
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertTrue(len(message['data']) == 0)

    def test_delete_results_endpoint_with_non_existing_result_id_throws_404(self):
        res = self.client().delete('/results/1', headers=basic_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_delete_results_endpoint_with_result_id_belonging_to_other_user_throws_403(self):
        post_data = {'test_id': self.create_test(), 'time': datetime.datetime.utcnow(), 'value': 3}

        res = self.client().post('/results', json=post_data, headers=basic_auth_header(True))
        data = json.loads(res.data)
        post_result = self.check_if_operation_was_successful_and_get_payload(data)

        res = self.client().delete('/results/' + str(post_result['id']), headers=advanced_auth_header(True))
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 403)

    def test_delete_results_endpoint_with_no_authorization_returns_401(self):
        res = self.client().delete('/results/1')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 401)
