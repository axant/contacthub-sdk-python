# -*- coding: utf-8 -*-
from contacthub.node import Node
from contacthub.parsers.config_parser import WorkspaceConfigParser


class Workspace(object):

    def __init__(self, workspace_id, token):
        self._workspace_id = workspace_id
        self._token = token

    @classmethod
    def from_ini_file(cls, file_path):
        options = WorkspaceConfigParser(file_path).get_options()
        workspace_id = options.get('workspace_id', '')
        token = options.get('token', '')
        if workspace_id and token:
            return Workspace(workspace_id=workspace_id,token=token)
        raise KeyError("workspace_id or token parameter not found in INI file")

    def get_node(self, node_id):
        return Node(self, node_id)



