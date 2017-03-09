import json
import unittest

import mock
from requests import HTTPError

from contacthub.APIManager.api_event import EventAPIManager
from contacthub.DeclarativeAPIManager.declarative_api_event import EventDeclarativeApiManager
from contacthub.models.event import Event
from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestEventAPIManager(unittest.TestCase):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.event_manager = EventAPIManager(w.get_node(123))
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/events'


    @classmethod
    def tearDown(cls):
        pass

    if __name__ == '__main__':
        unittest.main()

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_get_all_events(self, mock_get_all):
        params_expected = {'customerId': '123'}
        resp = self.event_manager.get_all(customer_id="123")
        mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)
        assert type(resp) is dict, type(resp)
        assert 'elements' in resp, resp
        assert type(resp['elements']) is list, type(resp['elements'])

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response", status_code=401))
    def test_get_all_events_unauthorized(self, mock_get_all):
        params_expected = {'customerId': '123'}
        try:
            self.event_manager.get_all(customer_id="123")
        except HTTPError as e:
            mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)


class TestEventDeclativeAPIManager(unittest.TestCase):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.event_declarative_manager = EventDeclarativeApiManager(w.get_node(123))
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/events'


    @classmethod
    def tearDown(cls):
        pass

    if __name__ == '__main__':
        unittest.main()

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_get_all_events(self, mock_get_all):
        params_expected = {'customerId': '123'}
        resp = self.event_declarative_manager.get_all(customer_id='123')
        mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)
        assert isinstance(resp, list), type(resp)
        assert isinstance(resp[0], Event), type(resp[0])

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response", status_code=401))
    def test_get_all_events_unauthorized(self, mock_get_all):
        params_expected = {'customerId': '123'}
        try:
            self.event_declarative_manager.get_all(customer_id="123")
        except Exception as e:
            mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)
            assert e.__class__ is HTTPError, e.__class__
