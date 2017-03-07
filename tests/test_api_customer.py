import unittest

import mock
from requests import HTTPError

from contacthub.workspace import Workspace
from contacthub.APIManager.api_customer import CustomerAPIManager
from tests.utility import FakeHTTPResponse


class TestNode(unittest.TestCase):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.customer_manager = CustomerAPIManager(w.get_node(123))


    @classmethod
    def tearDown(cls):
        pass

    if __name__ == '__main__':
        unittest.main()

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=200))
    def test_get_custumer(self, mock_get):
        resp = self.customer_manager.get_all()
        assert type(resp) is dict, type(resp)
        assert 'elements' in resp, resp

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=401))
    def test_get_customer_unathorized(self, mock_get):
        with self.assertRaises(HTTPError) as context:
            self.customer_manager.get_all()
        self.assertTrue('401' in str(context.exception))






