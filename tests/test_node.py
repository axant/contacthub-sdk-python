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
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'

    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_customers(self, mock_get):
        customers = self.node.get_customers()

        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        params_expected = {'nodeId': '123'}
        mock_get.assert_called_with(base_url, params=params_expected, headers=self.headers_expected)
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

        mock_get.assert_called_with(base_url, params=params_expected, headers=self.headers_expected)

        assert customers_query[0].base.contacts.email == 'marco.bosio@axant.it', customers_query[0].base.contacts.email
        assert customers_query[0].extra == 'Ciao', customers_query[0].extra

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_(self, mock_get):
        customers = self.node.get_customer(id='01')
        self.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers/01'
        mock_get.assert_called_with(base_url, headers=self.headers_expected)

    @mock.patch('requests.delete', return_value=FakeHTTPResponse())
    def test_delete_customer(self, mock_get):
        c = Customer(node=self.node, id='01')
        self.node.delete_customer(c)
        mock_get.assert_called_with(self.base_url + '/01', headers=self.headers_expected)

    @mock.patch('requests.post', return_value=FakeHTTPResponse())
    def test_add_customer(self, mock_get):
        c = Customer(node=self.node, base=Entity(contacts=Entity(email='email')))
        self.node.add_customer(customer=c)
        body = {'nodeId': self.node.node_id, 'base': {'contacts': {'email': 'email'}}, 'extended': {}, 'tags': {'auto': [], 'manual': []}}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, json=body)

    @mock.patch('requests.post', return_value=FakeHTTPResponse())
    def test_add_customer_extended(self, mock_get):
        c = Customer(node=self.node, base=Entity(contacts=Entity(email='email')))
        c.extended.prova = 'prova'
        self.node.add_customer(customer=c)
        body = {'nodeId': self.node.node_id, 'base': {'contacts': {'email': 'email'}}, 'extended': {'prova':'prova'},
                'tags': {'auto': [], 'manual': []}}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, json=body)

    @mock.patch('requests.post', return_value=FakeHTTPResponse())
    def test_add_customer_tags(self, mock_get):
        c = Customer(node=self.node, base=Entity(contacts=Entity(email='email')))
        c.extended.prova = 'prova'
        c.tags.auto = ['auto']
        c.tags.manual = ['manual']
        self.node.add_customer(customer=c)
        body = {'nodeId': self.node.node_id, 'base': {'contacts': {'email': 'email'}}, 'extended': {'prova': 'prova'},
                'tags': {'auto': ['auto'], 'manual': ['manual']}}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse())
    def test_update_customer_not_full(self, mock_patch):
        c = Customer(node=self.node, id='01', base=Entity(contacts=Entity(email='email')))
        c.extra = 'extra'
        self.node.update_customer(customer=c)
        body = {'extra': 'extra'}
        mock_patch.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)

    @mock.patch('requests.put', return_value=FakeHTTPResponse())
    def test_update_customer_full(self, mock_get):
        c = Customer(node=self.node, id='01', base=Entity(contacts=Entity(email='email', fax='fax')))
        c.base.contacts.email = 'email1234'
        self.node.update_customer(customer=c, full_update=True)
        body = {'id':'01', 'base': {'contacts': {'email': 'email1234', 'fax': 'fax'}}, 'extended': {},
                'tags': {'auto': [], 'manual': []}}
        mock_get.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)

    @mock.patch('requests.post',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_session_response'))
    def test_add_customer_session(self, mock_get):
        s_id = self.node.create_session_id()
        body = {'value': str(s_id)}

        self.node.add_customer_session(customer=Customer(id='01', node=self.node), session_id=s_id)
        mock_get.assert_called_with(self.base_url + '/01/sessions', headers=self.headers_expected, json=body)

    @mock.patch('requests.get',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_add_tag(self, mock_patch, mock_get):
        self.node.add_tag(customer=Customer(id='b6023673-b47a-4654-a53c-74bbc0204a20', node=self.node), tag='tag1')
        mock_get.assert_called_with(self.base_url + '/b6023673-b47a-4654-a53c-74bbc0204a20', headers=self.headers_expected)
        mock_patch.assert_called_with(self.base_url + '/b6023673-b47a-4654-a53c-74bbc0204a20', headers=self.headers_expected, json={'tags':{'manual':['manual','tag1']}})

    @mock.patch('requests.get',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_remove_tag(self, mock_patch, mock_get):
        self.node.remove_tag(customer=Customer(id='b6023673-b47a-4654-a53c-74bbc0204a20', node=self.node), tag='manual')
        mock_get.assert_called_with(self.base_url + '/b6023673-b47a-4654-a53c-74bbc0204a20',
                                    headers=self.headers_expected)
        mock_patch.assert_called_with(self.base_url + '/b6023673-b47a-4654-a53c-74bbc0204a20',
                                      headers=self.headers_expected, json={'tags': {'manual': []}})

    @mock.patch('requests.get',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_remove_tag_unexistent(self, mock_patch, mock_get):

        try:
            self.node.remove_tag(customer=Customer(id='b6023673-b47a-4654-a53c-74bbc0204a20', node=self.node), tag='asd')
            mock_get.assert_called_with(self.base_url + '/b6023673-b47a-4654-a53c-74bbc0204a20',
                                        headers=self.headers_expected)
        except ValueError as e:
            assert 'Tag' in str(e), str(e)