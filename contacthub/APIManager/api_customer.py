import requests
import json

from contacthub.APIManager.api_base import BaseAPIManager
from contacthub.parsers.config_parser import GeneralConfigParser


class CustomerAPIManager(BaseAPIManager):

    def __init__(self, node):
        super(CustomerAPIManager, self).__init__(node, 'customers')

    def get_all(self, external_id=None, fields=None, query=None, pagination=None):
        params = {'nodeId': self.node.node_id}
        resp = requests.get(self.request_url, params=params, headers=self.headers)
        return json.loads(resp.text)











