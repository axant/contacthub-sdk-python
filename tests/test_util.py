import unittest
from contacthub.lib.read_only_list import ReadOnlyList
import json

from contacthub.lib.utils import DateEncoder, get_dictionary_paths, generate_mutation_tracker


class TestEvent(unittest.TestCase):

    def setUp(cls):
        cls.list = [1, 2, 3]

    @classmethod
    def tearDown(cls):
        pass

    def test_read_only_list_iter(self):
        rol = ReadOnlyList(self.list)
        for i in rol:
            ret = i
        assert ret == 3, ret

    def test_read_only_list_repr(self):
        rol = ReadOnlyList(self.list)
        assert rol.__repr__() == [1,2,3].__repr__(), rol.__repr__()


    def test_read_only_list_len(self):
        rol = ReadOnlyList(self.list)
        assert len(rol) == 3, len(rol)

    def test_date_encoder(self):
        try:
            json.dumps(ReadOnlyList, cls=DateEncoder)
        except TypeError as e:
            assert 'JSON' in str(e)

    def test_get_dictionary_paths(self):
        a = {'b': {'c': {'d': 1, 'e': 2}, 'f': {'g': 1}}}

        paths_exp = [['b','c','d'], ['b','c','e'], ['b','f','g']]

        paths = []
        get_dictionary_paths(a, paths, [])

        assert paths == paths_exp, paths

    def test_generate_mutation_tracker(self):
        d1 = {'a': {'b': 'c', 'd': 'e'}, 'f': 'g'}
        d2 = {'a': {'beta': 'c'}}

        d_exp = {'a': {'beta': 'c', 'b': None, 'd': None}, 'f': None}
        tracker = generate_mutation_tracker(d1,d2)
        assert d_exp ==tracker, tracker







