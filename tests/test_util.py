import unittest
from contacthub.lib.read_only_list import ReadOnlyList
import json

from contacthub.lib.utils import DateEncoder


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






