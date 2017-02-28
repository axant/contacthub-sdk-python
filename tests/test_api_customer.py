from unittest import TestSuite

from contacthub.workspace import Workspace


class TestNode(TestSuite):

    @classmethod
    def setUp(cls):
        cls.workspace_id = '0aea7919-57cd-4260-910e-8b1ae53a7259'
        cls.node_id = '91316725-a4c2-420b-a3f3-2556b3630444'
        cls.token = 'dcf93c15263a44df842a22086c6087d5bf9c01cd9540451b871175eb570e7794'

    @classmethod
    def tearDown(cls):
        pass

    def test_get_custumer(self):
        pass





