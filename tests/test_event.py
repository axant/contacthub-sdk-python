import unittest

import mock

from contacthub.lib.read_only_list import ReadOnlyList
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
        cls.customer = cls.node.get_customers()[0]
        cls.events = cls.customer.events

    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_event_response'))
    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_event_from_customers(self, mock_get_customers, mock_get_events):
        events = self.node.get_customers()[0].events
        assert isinstance(events, ReadOnlyList), type(events)
        assert isinstance(events[0], Event), type(events[0])
        try:
            events.append(Event())
        except ValueError as e:
            assert 'Read Only' in str(e)

    def test_get_properties(self):
        prop = self.events[0].properties
        assert isinstance(prop, dict), type(prop)

    def test_get_unexsistent(self):
        try:
            prop = self.events[0].attr
        except AttributeError as e:
            assert 'attr' in str(e), str(e)

    def test_create_new_event_properties(self):
        e = Event()
        assert isinstance(e.properties, dict), type(e.properties)
        e.properties = Properties(attr='attr')
        assert e.properties.attr == 'attr'

    def test_set_event_properties(self):
        e = self.events[0]
        assert isinstance(e.properties, dict)
        e.context = Event.CONTEXTS.DIGITAL_CAMPAIGN
        assert e.context == Event.CONTEXTS.DIGITAL_CAMPAIGN, e.context


