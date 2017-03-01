import requests
import json
from contacthub.parsers.config_parser import GeneralConfigParser


class CustomerAPIManager(object):

    def __init__(self, node):
        self.node = node
        self.entity = 'customers'
        self.request_url = self.node.workspace.base_url + '/' + self.node.workspace.workspace_id + '/' + self.entity
        self.headers = {'Authorization': 'Bearer ' + self.node.workspace.token}

    def get_all(self, external_id=None, fields=None, query=None, pagination=None):
        params = {'nodeId': self.node.node_id}
        resp = requests.get(self.request_url, params=params, headers=self.headers)
        return json.loads(resp.text)











