import json

import datetime


def list_item(_class, JSON_list):
    """
    Create a list of objects from a JSON formatted list
    :param _class: The class for instantiate objects in the list
    :param JSON_list: A JSON formatted list
    :return: A list of specified objects, wich will receive as parameter the elements of the JSON list
    """
    obj_list_ret = []
    for elements in JSON_list:
        obj_list_ret.append(_class(elements))
    return obj_list_ret


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)