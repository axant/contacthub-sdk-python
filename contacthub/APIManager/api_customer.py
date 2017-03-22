import requests
import json

from requests import HTTPError

from contacthub.APIManager.api_base import BaseAPIManager
from contacthub.models.query.entity_meta import EntityMeta
from contacthub.lib.utils import DateEncoder

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
            params['query'] = json.dumps(query, cls=DateEncoder)
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
        resp = requests.get(self.request_url + '/' + str(_id), headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))

    def post(self, body, urls_extra=None, force_update=False):
        """
        POST a new customer in /customers
        :param data: the JSON format body for posting the new customer
        :return: a JSON format loaded representing the respnse from the API
        """
        if not urls_extra:
            body['nodeId'] = self.node.node_id
            request_url = self.request_url
        else:
            request_url = self.request_url + urls_extra
        resp = requests.post(request_url, json=body, headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        if resp.status_code == 409 and force_update:
            body.pop('nodeId')
            return self.patch(_id=response_text['data']['customer']['id'], body=body)
        raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))

    def delete(self, _id):
        """
        Delete a customer in /customers by its id
        :param _id: the id of the customer to delete
        :return: a JSON format loaded representing the respnse from the API
        """
        resp = requests.delete(self.request_url + '/' + str(_id), headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))

    def patch(self, _id, body):
        """
        PATCH a  customer in /customers
        :param _id:
        :param body: the JSON format body for patching the customer
        :return: a JSON format loaded representing the respnse from the API
                """

        body = json.dumps(body, cls=DateEncoder)
        resp = requests.patch(self.request_url + '/' + str(_id), json=json.loads(body), headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))

    def put(self, _id, body):
        """
        PATCH a  customer in /customers
        :param _id:
        :param body: the JSON format body for patching the customer
        :return: a JSON format loaded representing the respnse from the API
                """
        resp = requests.put(self.request_url + '/' + str(_id), json=body, headers=self.headers)
        response_text = json.loads(resp.text)
        if 200 <= resp.status_code < 300:
            return response_text
        raise HTTPError("Code: %s, message: %s" % (resp.status_code, response_text))
















