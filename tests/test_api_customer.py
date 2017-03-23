import unittest
from unittest import TestSuite

import mock
from contacthub.models import Entity
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
        cls.node = w.get_node(123)
        cls.customer_manager = CustomerAPIManager(node=cls.node)
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'


    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=200))
    def test_get_all_custumers(self, mock_get):
        params_expected = {'nodeId': '123'}
        resp = self.customer_manager.get_all()
        mock_get.assert_called_with(self.base_url, params=params_expected, headers=self.headers_expected)
        assert type(resp) is dict, type(resp)
        assert 'elements' in resp, resp

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=401))
    def test_get_customer_unathorized(self, mock_get):
        params_expected = {'nodeId': '123'}
        try:
            self.customer_manager.get_all()
        except HTTPError as e:
            mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)


    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response'))
    def test_post_customer(self, mock_get):
        body = {'base': {'contacts': {'email': 'email@email.it'}}}
        data_expected = {'base': {'contacts': {'email': 'email@email.it'}}, 'nodeId': '123'}

        self.customer_manager.post(body=body)
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, json  =data_expected)

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response', status_code=401))
    def test_post_customer_unathorized(self, mock_get):
        try:
            self.customer_manager.post(body={})
        except HTTPError as e:
            assert 'message' in str(e), str(e)

    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response', status_code=401))
    def test_patch_customer_unathorized(self, mock_get):
        try:
            self.customer_manager.patch(_id='id', body={})
        except HTTPError as e:
            assert 'message' in str(e), str(e)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response'))
    def test_put_customer(self, mock_get):
        body = {'base': {'contacts': {'email': 'email@email.it'}}}

        self.customer_manager.put(_id='01', body=body)
        mock_get.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response', status_code=400))
    def test_put_customer_unauthorized(self, mock_get):
        try:
            self.customer_manager.put(_id='id', body={})
        except HTTPError as e:
            assert 'message' in str(e), str(e)



class TestCustomerDeclarativeApiManager(TestSuite):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.node = w.get_node(123)
        cls.customer_manager = CustomerDeclarativeApiManager(node=w.get_node(123), entity=Customer)
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'

    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=200))
    def test_get_all_custumers(self, mock_get):
        params_expected = {'nodeId': '123'}
        customers = self.customer_manager.get_all()
        mock_get.assert_called_with(self.base_url, params=params_expected, headers=self.headers_expected)
        assert type(customers) is list, type(customers)
        assert isinstance(customers[0], Customer), type(customers[0])

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_post_customer(self, mock_get):
        body = {'extra': 'extra', 'base': {'contacts': {'email': 'email@email.email'}}}
        data_expected = {'base': {'contacts': {'email': 'email@email.email'}}, 'extra': 'extra', 'extended': {},
                         'tags': {'auto': [], 'manual': []}, 'nodeId': '123'}
        c = Customer(node=self.node, **body)
        posted = self.customer_manager.post(customer=c)
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, json=data_expected)
        assert isinstance(posted, Customer), type(posted)
        assert posted.base.contacts.email == 'email@email.email', posted.base.contacts.email
        assert posted.extra == 'extra', posted.extra

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_all_custumers_external_id(self, mock_get):
        params_expected = {'nodeId': '123','externalId':'02'}
        customers = self.customer_manager.get_all(externalId='02')
        mock_get.assert_called_with(self.base_url, params=params_expected, headers=self.headers_expected)
        assert type(customers) is list, type(customers)
        assert isinstance(customers[0], Customer), type(customers[0])

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_all_custumers_page_size(self, mock_get):
        params_expected = {'nodeId': '123', 'page': 2, 'size':10}
        customers = self.customer_manager.get_all(page=2, size=10)
        mock_get.assert_called_with(self.base_url, params=params_expected, headers=self.headers_expected)
        assert type(customers) is list, type(customers)
        assert isinstance(customers[0], Customer), type(customers[0])

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_get(self, mock_get):
        customers = self.customer_manager.get(id='01')
        mock_get.assert_called_with(self.base_url + '/01', headers=self.headers_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_external_id(self, mock_get):
        customers = self.customer_manager.get(externalId='01')
        params = {'nodeId': '123', 'externalId':'01'}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response'))
    def test_get_external_id_alone(self, mock_get):
        customers = self.customer_manager.get(externalId='01')
        params = {'nodeId': '123', 'externalId': '01'}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=400))
    def test_get_error(self, mock_get):
        try:
            customers = self.customer_manager.get(id='01')
        except HTTPError as e:
            assert 'message' in str(e)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=400))
    def test_get_all_error(self, mock_get):
        try:
            customers = self.customer_manager.get_all()
        except HTTPError as e:
            assert 'message' in str(e)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=400))
    def test_get_id_and_external_id(self, mock_get):
        try:
            customers = self.customer_manager.get(id='01', externalId='02')
        except ValueError as e:
            assert 'id' in str(e)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=400))
    def test_get_no_id_and_external_id(self, mock_get):
        try:
            customers = self.customer_manager.get()
        except ValueError as e:
            assert 'id' in str(e)

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_conflict_response', status_code=409))
    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response', status_code=200))
    def test_post_with_patch(self, mock_patch, mock_post):
        body = {'extra': 'extra', 'base': {'contacts': {'email': 'email@email.email'}}}
        c = Customer.from_dict(node=self.node, properties=body)
        posted = self.customer_manager.post(customer=c, force_update=True)
        mock_patch.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)

    @mock.patch('requests.put',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_put(self, mock_put):
        body = {'id':'01','extra': 'extra', 'base': {'contacts': {'email': 'email@email.email'}}, 'extended': {},
                'tags': {'auto': [], 'manual': []}}
        c = Customer(id='01', node=self.node, extra='extra', base=Entity(contacts=Entity(email='email@email.email')))

        self.customer_manager.put(customer=c)
        mock_put.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)

    @mock.patch('requests.put',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_put_timezone(self, mock_put):
        body = {'extra': 'extra', 'base': {'timezone': None, 'contacts': {'email': 'email@email.email'}}}
        c = Customer(node=self.node,**body)
        c.id = '01'

        body = {'id':'01','extra': 'extra', 'base': {'timezone': 'Europe/Rome', 'contacts': {'email': 'email@email.email'}}, 'extended': {},
                'tags': {'auto': [], 'manual': []}}

        self.customer_manager.put(customer=c)
        mock_put.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)

    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch(self, mock_put):
        body = { 'base':{'contacts':{'email':'altraemail'}}}
        c = Customer(id='01', node=self.node, extra='extra', base=Entity(contacts=Entity(email='email@email.email')))

        c.base.contacts.email = 'altraemail'

        self.customer_manager.patch(customer=c)
        mock_put.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)
        assert c.mute == {'base.contacts.email':'altraemail'}

    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_multiplefield(self, mock_put):
        body = {'base': {'firstName': 'firstName', 'lastName': 'lastName'}}
        c = Customer(id='01', node=self.node, extra='extra', base=Entity(firstName='first', lastName='last'))

        c.base.firstName = 'firstName'
        c.base.lastName = 'lastName'

        self.customer_manager.patch(customer=c)
        mock_put.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)
        assert c.mute == {'base.firstName': 'firstName', 'base.lastName':'lastName'}

    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_list(self, mock_put):
        body = {'base': {'contacts': {'otherContacts':[{'type':'MOBILE', 'name':'otherName', 'value': 'value'},
                                                       {'type':'MOBILE', 'name':'otherName1', 'value': 'value1'}]}}}
        c = Customer(id='01', node=self.node, extra='extra', base=Entity(contacts=Entity(otherContacts=[{'type':'MOBILE', 'name':'name', 'value': 'value'},
                                                                                                        {'type':'MOBILE', 'name':'name1', 'value': 'value1'}])))

        c.base.contacts.otherContacts[0].name = 'otherName'
        c.base.contacts.otherContacts[1].name = 'otherName1'

        self.customer_manager.patch(customer=c)
        mock_put.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)
        assert c.mute == {'base.contacts.otherContacts': [{'type':'MOBILE', 'name':'otherName', 'value': 'value'},
                                                        {'type':'MOBILE', 'name':'otherName1', 'value': 'value1'}]}

    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_full_list(self, mock_put):
        body = {'base': {'contacts': {'otherContacts':  [{'type': 'MOBILE', 'name': 'otherName', 'value': 'otherValue'}]}}}
        c = Customer(id='01', node=self.node, extra='extra',
                     base=Entity(contacts=Entity(otherContacts=[{'type': 'MOBILE', 'name': 'name', 'value': 'value'},
                                                                {'type': 'MOBILE', 'name': 'name1',
                                                                 'value': 'value1'}])))

        c.base.contacts.otherContacts = [{'type': 'MOBILE', 'name': 'otherName', 'value': 'otherValue'}]

        self.customer_manager.patch(customer=c)
        mock_put.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)
        assert c.mute == {'base.contacts.otherContacts':  [{'type': 'MOBILE', 'name': 'otherName', 'value': 'otherValue'}]}














