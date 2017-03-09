import json
from unittest import TestSuite

import mock

from contacthub.models import Contacts
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
        headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        params_expected = {'query': '', 'nodeId': '123'}
        mock_get.assert_called_with(base_url, params=params_expected, headers=headers_expected)
        assert type(customers) is list, type(customers)
        assert customers[0].enabled, customers[0]

    @mock.patch('contacthub.APIManager.api_customer.CustomerAPIManager.get_all')
    def test_query(self, mock_get):
        mock_get.return_value = json.loads(FakeHTTPResponse(resp_path='tests/util/fake_query_response').text)
        query_expected = {'query':
                               {'type': 'simple', 'name': 'query', 'are':
                                   {'condition':
                                        {'type': 'composite', 'conjunction': 'and', 'conditions': [
                                            {'type': 'atomic', 'attribute': 'base.contacts.email', 'operator': 'EQUALS',
                                             'value': 'marco.bosio@axant.it'},
                                            {'type': 'atomic', 'attribute': 'extra', 'operator': 'EQUALS',
                                             'value': 'Ciao'}
                                        ]}
                                    }
                                }
                           }
        customers_query = self.node.query(Customer).filter((Customer.base.contacts.email == 'marco.bosio@axant.it') & (Customer.extra == 'Ciao')).all()
        mock_get.assert_called_with(query=query_expected)
        assert customers_query[0].base.contacts.email == 'marco.bosio@axant.it', customers_query[0].base.contacts.email
        assert customers_query[0].extra == 'Ciao', customers_query[0].extra

    @mock.patch('contacthub.APIManager.api_customer.CustomerAPIManager.post')
    def test_post_customer_first_method(self, mock_post):
        expected_body = {'base': {'contacts': {'email': 'email@email.email'}}, 'extra': 'extra'}
        mock_post.return_value = json.loads(FakeHTTPResponse(resp_path='tests/util/fake_post_response').text)
        c = Customer()
        c.base.contacts.email = 'email@email.email'
        c.extra = 'extra'
        posted = self.node.post(c)
        mock_post.assert_called_with(body=expected_body)
        assert isinstance(posted, Customer), type(posted)
        assert posted.base.contacts.email == c.base.contacts.email, posted.base.contacts.email
        assert posted.extra == c.extra, posted.extra

    @mock.patch('contacthub.APIManager.api_customer.CustomerAPIManager.post')
    def test_post_customer_second_method(self, mock_post):
        expected_body = {'base': {'contacts': {'email': 'email@email.email'}}, 'extra': 'extra'}
        mock_post.return_value = json.loads(FakeHTTPResponse(resp_path='tests/util/fake_post_response').text)
        c = Customer()
        c.base.contacts = Contacts(email='email@email.email')
        c.extra = 'extra'
        posted = self.node.post(c)
        mock_post.assert_called_with(body=expected_body)
        assert isinstance(posted, Customer), type(posted)
        assert posted.base.contacts.email == c.base.contacts.email, posted.base.contacts.email
        assert posted.extra == c.extra, posted.extra

    @mock.patch('contacthub.APIManager.api_customer.CustomerAPIManager.post')
    def test_post_customer_third_method(self, mock_post):
        expected_body = {'base': {'contacts': {'email': 'email@email.email'}}, 'extra': 'extra'}
        mock_post.return_value = json.loads(FakeHTTPResponse(resp_path='tests/util/fake_post_response').text)
        c = Customer()
        c.base.contacts = {'email': 'email@email.email'}
        c.extra = 'extra'
        posted = self.node.post(c)
        mock_post.assert_called_with(body=expected_body)
        assert isinstance(posted, Customer), type(posted)
        assert posted.base.contacts.email == c.base.contacts.email, posted.base.contacts.email
        assert posted.extra == c.extra, posted.extra