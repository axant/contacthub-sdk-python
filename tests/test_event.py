import unittest

import mock

from contacthub.models import Entity, Properties
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
        cls.customer = cls.node.customers[0]
        cls.events = cls.customer.all_events()

    @classmethod
    def tearDown(cls):
        pass

    def test_get_properties(self):
        prop = self.events[0].properties
        assert isinstance(prop, Entity), type(prop)

    def test_get_unexsistent(self):
        try:
            prop = self.events[0].attr
        except AttributeError as e:
            assert 'attr' in str(e), str(e)

    def test_create_new_event_properties(self):
        e = Event()
        assert isinstance(e.properties, Entity)
        e.properties = Properties(attr='attr')
        assert e.properties.attr == 'attr'

    def test_set_event_properties(self):
        e = self.events[0]
        assert isinstance(e.properties, Entity)
        e.context = Event.CONTEXTS.DIGITAL_CAMPAIGN
        assert e.context == Event.CONTEXTS.DIGITAL_CAMPAIGN, e.context


