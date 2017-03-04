from unittest import TestSuite

import mock

from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestNode(TestSuite):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.node = w.get_node(123)

    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_customers(self, mock_get):
        customers = self.node.customers
        assert type(customers) is list, type(customers)
        assert customers[0].enabled, customers[0]