import unittest

import mock

from contacthub.lib.read_only_list import ReadOnlyList
from contacthub.models import Property, Properties
from contacthub.models.customer import Customer
from contacthub.models.education import Education
from contacthub.models.event import Event
from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestEvent(unittest.TestCase):

    @classmethod
    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_event_response'))
    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def setUp(cls, mock_get_customers, mock_get_events):
        w = Workspace(workspace_id="123", token="456")
        cls.node = w.get_node("123")
        cls.customers = cls.node.get_customers()
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url_customer = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        cls.education = Education(customer=Customer(id='01', node=cls.node), **{'id':'01'})

    @classmethod
    def tearDown(cls):
        pass


    @mock.patch('requests.post', return_value=FakeHTTPResponse())
    def test_post(self, mock_post):
        pass


