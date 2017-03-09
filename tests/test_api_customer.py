import unittest
from unittest import TestSuite

import mock
from requests import HTTPError

from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager
from contacthub.models.customer import Customer
from contacthub.workspace import Workspace
from contacthub.APIManager.api_customer import CustomerAPIManager
from tests.utility import FakeHTTPResponse


class TestCustomerAPIManager(TestSuite):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.customer_manager = CustomerAPIManager(w.get_node(123))
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'


    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=200))
    def test_get_all_custumers(self, mock_get):
        params_expected = {'nodeId': '123', 'query': ''}
        resp = self.customer_manager.get_all()
        mock_get.assert_called_with(self.base_url, params=params_expected, headers=self.headers_expected)
        assert type(resp) is dict, type(resp)
        assert 'elements' in resp, resp

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=401))
    def test_get_customer_unathorized(self, mock_get):
        params_expected = {'nodeId': '123', 'query': ''}
        try:
            self.customer_manager.get_all()
        except HTTPError as e:
            mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)


    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response'))
    def test_post_customer(self, mock_get):
        body = {'base': {'contacts': {'email': 'email@email.it'}}}
        data_expected = {'base': {'contacts': {'email': 'email@email.it'}}, 'nodeId': '123'}

        self.customer_manager.post(body=body)
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, data=data_expected)


    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response', status_code=401))
    def test_post_customer_unathorized(self, mock_get):
        body = {'base': {'contacts': {'email': 'email@email.it'}}}
        data_expected = {'base': {'contacts': {'email': 'email@email.it'}}, 'nodeId': '123'}
        try:
            self.customer_manager.post(body=body)
        except HTTPError as e:
            mock_get.assert_called_with(self.base_url, headers=self.headers_expected, data=data_expected)



class TestCustomerDeclarativeApiManager(TestSuite):
    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.customer_manager = CustomerDeclarativeApiManager(w.get_node(123))
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'

    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=200))
    def test_get_all_custumers(self, mock_get):
        params_expected = {'nodeId': '123', 'query': ''}
        customers = self.customer_manager.get_all()
        mock_get.assert_called_with(self.base_url, params=params_expected, headers=self.headers_expected)
        assert type(customers) is list, type(customers)
        assert isinstance(customers[0], Customer), type(customers[0])

    @mock.patch('requests.post', return_value=FakeHTTPResponse(status_code=200, resp_path='tests/util/fake_post_response'))
    def test_post_customer(self, mock_get):
        body = {'extra': 'extra', 'base': {'contacts': {'email': 'email@email.email'}}}
        data_expected = {'extra': 'extra', 'base': {'contacts': {'email': 'email@email.email'}}, 'nodeId': '123'}
        c = Customer(json_properties=body)
        posted = self.customer_manager.post(customer=c)
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, data=data_expected)
        assert isinstance(posted, Customer), type(posted)
        assert posted.base.contacts.email == 'email@email.email', posted.base.contacts.email
        assert posted.extra == 'extra', posted.extra







