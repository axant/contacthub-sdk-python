import json

import requests
from requests import HTTPError

from contacthub.APIManager.api_base import BaseAPIManager


class EventAPIManager(BaseAPIManager):
    """
    A wrapper for the orginal API regarding the events data. This is the lowest level for retrieving data from the API.
    """

    def __init__(self, node):
        """
        :param node: the Node object for retrieving Events data
        """
        super(EventAPIManager, self).__init__(node, 'events')

    def get_all(self, customer_id, type=None, context=None, mode=None, dateFrom=None, dateTo=None, *args, **kwargs):
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
        resp = requests.get(self.request_url, params=params, headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))

    # def post(self, *args, **kwargs):
    #     pass













