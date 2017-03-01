from unittest import TestSuite

from mock import mock

from contacthub.workspace import Workspace
from contacthub.APIManager.api_customer import CustomerAPIManager
from tests.utility import FakeHTTPResponse

class TestNode(TestSuite):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.customer_manager = CustomerAPIManager(w.get_node(123))


    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_custumer(self, mock_get):
        resp = self.customer_manager.get_all()
        assert type(resp) is dict, type(resp)
        assert 'elements' in resp, resp






