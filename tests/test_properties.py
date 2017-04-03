import unittest

from contacthub import Workspace
from contacthub.models import Properties
from contacthub.models.customer import Customer


class TestProperties(unittest.TestCase):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id="123", token="456")
        cls.node = w.get_node("123")

    @classmethod
    def tearDown(cls):
        pass

    def test_properties_from_dict_empty(self):
        p = Properties.from_dict()
        assert p.attributes == {}, p.attributes

    def test_generate_mutation_tracker_new(self):
        p = Properties(parent=Customer(node=self.node))
        p.prova = Properties(a='b')
        assert p.mute == {'prova': {'a': 'b'}}, p.mute

