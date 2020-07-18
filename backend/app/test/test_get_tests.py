import json

from app.test.base_test_class import BaseTestClass


class GetTestsTestCase(BaseTestClass):

    def test_get_tests_returns_list_of_tests(self):
        self.add_data_to_database([
            {'test': 1, 'user': 1, 'data': 10},
            {'test': 2, 'user': 2, 'data': 10}])
        res = self.client().get('/tests')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertTrue(len(message) == 2)
        test_names = []
        for test in message:
            test_names.append(test['name'])
        self.assertTrue('Test1' in test_names)
        self.assertTrue('Test2' in test_names)
