import json

from app.test.base_test_class import BaseTestClass


class GetTestsTestCase(BaseTestClass):

    def test_get_tests_returns_list_of_tests(self):
        res = self.client().get('/tests')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)