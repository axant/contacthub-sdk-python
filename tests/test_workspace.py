from contacthub.workspace import Workspace, Node
from unittest import TestSuite


class TestWorkspace(TestSuite):

    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def tearDown(cls):
        pass

    def test_workspace_from_ini_file(self):
        w = Workspace.from_ini_file('tests/util/config.ini')
        assert w._workspace_id == str(123), w._workspace_id
        assert w._token == str(456), w._token

    def test_get_node(self):
        w = Workspace('123', '456')
        n = Node(w, 'nodo')
        assert w.get_node('nodo')._node_id == n._node_id
        assert w.get_node('nodo')._workspace == n._workspace