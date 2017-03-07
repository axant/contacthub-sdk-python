from unittest import TestSuite

import mock

from contacthub.models.customer import Customer
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

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response'))
    def test_query(self, mock_get):
        customers_query = self.node.query(Customer).filter((Customer.base.contacts.email == 'marco.bosio@axant.it') & (Customer.extra == 'Ciao')).all()
        assert customers_query[0].base.contacts.email == 'marco.bosio@axant.it', customers_query[0].base.contacts.email
        assert customers_query[0].extra == 'Ciao', customers_query[0].extra