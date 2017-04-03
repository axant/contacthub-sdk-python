import json

from datetime import datetime
import requests
from requests import HTTPError

from contacthub.api_manager.api_base import BaseAPIManager


class EventAPIManager(object):
    """
    A wrapper for the orginal API regarding the events data. This is the lowest level for retrieving data from the API.
    """

    def __init__(self, node):
        """
        :param node: the Node object for retrieving Events data
        """
        self.node = node
        self.request_url = self.node.workspace.base_url + '/' + self.node.workspace.workspace_id + '/events'
        self.headers = {'Authorization': 'Bearer ' + self.node.workspace.token, 'Content-Type': 'application/json'}

    def get_all(self, customer_id, type=None, context=None, mode=None, dateFrom=None, dateTo=None, page=None, size=None):
        """
       Retrieve all the events of the associated Node from the API.

        :param customer_id: The id of the customer owner of the event
        :param type: the type of the event present in Event.TYPES
        :param context: the context of the event present in Event.CONTEXT
        :param mode: the mode of event. ACTIVE if the customer made the event, PASSIVE if the customer recive the event
        :param dateFrom: From datetime for search of event
        :param dateTo: From datetime for search of event
        :return: A dictionary representing the JSON response from the API called if there were no errors,
                else raise an HTTPException

       """
        params = {'customerId': customer_id}
        if type:
            params['type'] = type
        if context:
            params['context'] = context
        if mode:
            params['mode'] = mode
        if dateFrom:
            if isinstance(dateFrom, datetime):
                date_from = dateFrom.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                date_from = dateFrom
            params['dateFrom'] = date_from
        if dateTo:
            if isinstance(dateTo, datetime):
                date_to = dateTo.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                date_to = dateTo
            params['dateTo'] = date_to
        if page:
            params['page'] = page
        if size:
            params['size'] = size
        resp = requests.get(self.request_url, params=params, headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))

    def get(self, _id):
        """
        Get the event associated to the given id
        :param _id: the id of the event to retrieve
        :return: A dictionary representing the JSON response from the API called if there were no errors,
                else raise an HTTPException
        """
        resp = requests.get(self.request_url + '/' + _id, headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))

    def post(self, body):
        """
        Post a new event with the given body
        :param body: the attributes associated to the event to post
        :return: A dictionary representing the JSON response from the API called if there were no errors,
                else raise an HTTPException
        """
        resp = requests.post(self.request_url, headers=self.headers, json=body)
        if resp.text:
            response_text = json.loads(resp.text)
            if 200 <= resp.status_code < 300:
                return response_text
            raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))













