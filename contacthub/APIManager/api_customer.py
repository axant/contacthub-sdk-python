import requests
import json

from requests import HTTPError

from contacthub.APIManager.api_base import BaseAPIManager
from contacthub.models.query.entity_meta import EntityMeta


class CustomerAPIManager(BaseAPIManager):
    """
    A wrapper for the orginal API regarding the customers data. This is the lowest level for retrieving data from the API.
    """

    def __init__(self, node):
        """
        Indicates at the BaseAPIManager that this class operate on customers.
        :param node: the Node object for retrieving customers data
        """
        super(CustomerAPIManager, self).__init__(node, EntityMeta.Enitites.CUSTOMERS)

    def get_all(self, externalId=None, fields=None, query=None, size=None, page=None, **kwargs):
        """
        Get method on /customers for all the customers of the associated Node from the API.

        :param size:
        :param external_id:
        :param fields:
        :param query: A JSON format query for filter the custumers data
        :return: A dictionary representing the JSON response from the API called if there were no errors,
                else raise an HTTPException
        """
        params = {'nodeId': self.node.node_id}
        if query:
            params['query'] = json.dumps(query)
        if externalId:
            params['externalId'] = str(externalId)
        if size:
            params['size'] = size
        if page:
            params['page'] = page

        resp = requests.get(self.request_url, params=params, headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        raise HTTPError("Code: %s, message: %s" %(resp.status_code, response_text))

    def get(self, _id):
        url = self.request_url + '/' + _id
        resp = requests.get(url, headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))

    def post(self, body):
        """
        POST a new customer in /customers
        :param data: the JSON format body for posting the new customer
        :return:
        """
        body['nodeId'] = self.node.node_id
        resp = requests.post(self.request_url, data=body, headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))














