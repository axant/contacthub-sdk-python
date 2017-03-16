import json
from unittest import TestSuite

import mock

from contacthub.models import Contacts
from contacthub.models import Entity
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
    def test_get_all_customers(self, mock_get):
        customers = self.node.get_all_customers()
        headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        params_expected = {'nodeId': '123'}
        mock_get.assert_called_with(base_url, params=params_expected, headers=headers_expected)
        assert type(customers) is list, type(customers)
        assert customers[0].enabled, customers[0]

    @mock.patch('requests.get')
    def test_query(self, mock_get):
        mock_get.return_value = FakeHTTPResponse(resp_path='tests/util/fake_query_response')
        query_expected = {'name':'query', 'query':
                               {'type': 'simple', 'name': 'query', 'are':
                                   {'condition':
                                        {'type': 'composite', 'conditions': [
                                            {'type': 'atomic', 'attribute': 'base.contacts.email', 'operator': 'EQUALS',
                                             'value': 'marco.bosio@axant.it'},
                                            {'type': 'atomic', 'attribute': 'extra', 'operator': 'EQUALS',
                                             'value': 'Ciao'}
                                        ], 'conjunction': 'and'}
                                    }
                                }
                           }

        customers_query = self.node.query(Customer).filter((Customer.base.contacts.email == 'marco.bosio@axant.it') & (Customer.extra == 'Ciao')).all()
        params_expected = {'nodeId': '123','query': json.dumps(query_expected) }
        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}

        mock_get.assert_called_with(base_url, params=params_expected, headers=headers_expected)

        assert customers_query[0].base.contacts.email == 'marco.bosio@axant.it', customers_query[0].base.contacts.email
        assert customers_query[0].extra == 'Ciao', customers_query[0].extra



    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_(self, mock_get):
        customers = self.node.get_customer(id='01')
        headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers/01'
        mock_get.assert_called_with(base_url, headers=headers_expected)