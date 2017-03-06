import requests
import json

from contacthub.APIManager.api_base import BaseAPIManager
from contacthub.parsers.config_parser import GeneralConfigParser


class CustomerAPIManager(BaseAPIManager):
    """
    A wrapper for the orginal API regarding the customers data. This is the lowest level for retrieving data from the API.
    Implements the BaseAPIManager class
    """

    def __init__(self, node):
        """
        Indicates at the BaseAPIManager that this class operate on customers.
        :param node: the Node object for retrieving customers data
        """
        super(CustomerAPIManager, self).__init__(node, 'customers')

    def get_all(self, external_id=None, fields=None, query=None, pagination=None):
        """
        Retrieve all the customers of the associated Node from the API.

        :param external_id:
        :param fields:
        :param query: A JSON format string representing the query for filter the custumers data
        :param pagination:
        :return: A dictionary representing the JSON response from the API called if there were no errors,
                else raise an HTTPException
        """
        params = {'nodeId': self.node.node_id, 'query':  query if not None else ''}
        resp = requests.get(self.request_url, params=params, headers=self.headers)
        if resp.status_code == 200:
            return json.loads(resp.text)
        resp.raise_for_status()











