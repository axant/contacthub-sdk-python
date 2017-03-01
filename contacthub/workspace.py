# -*- coding: utf-8 -*-
from contacthub.node import Node
from contacthub.parsers.config_parser import GeneralConfigParser


class Workspace(object):

    def __init__(self, workspace_id, token, base_url='https://api.contactlab.it/hub/v1/workspaces'):
        self.workspace_id = str(workspace_id)
        self.token = str(token)
        self.base_url = str(base_url)


    @classmethod
    def from_ini_file(cls, file_path):
        options = GeneralConfigParser(file_path).get_options()
        workspace_id = options.get('workspace_id', '')
        token = options.get('token', '')
        base_url = options.get('base_url', '')
        if workspace_id and token:
            if base_url:
                return Workspace(workspace_id=workspace_id, token=token, base_url=base_url)
            else:
                return Workspace(workspace_id=workspace_id, token=token)
        raise KeyError("workspace_id or token parameter not found in INI file")

    def get_node(self, node_id):
        return Node(self, node_id)



