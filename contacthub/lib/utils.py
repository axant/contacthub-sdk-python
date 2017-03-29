import json

import datetime

from copy import deepcopy


def list_item(_class, JSON_list):
    """
    Create a list of objects from a JSON formatted list
    :param _class: The class for instantiate objects in the list
    :param JSON_list: A JSON formatted list
    :return: A list of specified objects, wich will receive as parameter the elements of the JSON list
    """
    obj_list_ret = []
    for elements in JSON_list:
        obj_list_ret.append(_class(**elements))
    return obj_list_ret


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%SZ")
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        from contacthub.models import Property
        if isinstance(obj, Property):
            return obj.attributes
        return json.JSONEncoder.default(self, obj)


def get_dictionary_paths(d, main_list, tmp_list):
    """
    Set the given main_list with lists containing all the key-paths of a dictionary
    For example: The key-paths of this list {a{b:{c:1, d:2}, e:3}} are a,b,c; a,b,d; a,e
    :param d: the dictionary for gaining all the depth path
    :param main_list: a list for creating al the lists containing the paths of the dictt
    :param tmp_list: a temporary list for inserting the actual path
    """
    for elem in d:
        if isinstance(d[elem], dict):
            tmp_list.append(elem)
            get_dictionary_paths(d[elem], main_list=main_list, tmp_list=tmp_list)
            tmp_list.pop()
        else:
            tmp_list.append(elem)
            main_list.append(deepcopy(tmp_list))
            tmp_list.pop()


def generate_mutation_tracker(old_properties, new_properties):
    """
    Given the old properties of an Property and the new ones, create a new dictionary with all old properties:
        - the ones in new_properties updated
        - the ones not in new_properties setted to None
    :param old_properties: The old properties of an entity for create mutation
    :param new_properties: The new properties of an entity for create mutation
    :return: a dictionary with the mutation betweeen old_properties and new_properties
    """
    main_list_of_paths = []
    tmp_list_for_path = []

    get_dictionary_paths(old_properties, main_list=main_list_of_paths,
                         tmp_list=tmp_list_for_path)
    #  we start wih the whole old dictionary, next we will set the missing keys to None
    mutation_tracker = deepcopy(old_properties)
    #  follow the paths for searching keys not in new properties but in the old ones (mutation_tracker)

    for key_paths in main_list_of_paths:
        np = new_properties
        mt = mutation_tracker
        op = old_properties
        for single_key in key_paths:
            if single_key not in np:
                if single_key in op and isinstance(op[single_key], list):
                    mt[single_key] = []
                else:
                    mt[single_key] = None
                break
            else:
                mt[single_key] = np[single_key]
                np = np[single_key]
                mt = mt[single_key]
                op = op[single_key]
    return mutation_tracker


def convert_properties_obj_in_prop(properties, property):
    for k in properties:
        if isinstance(properties[k], property):
            properties[k] = properties[k].attributes
        elif isinstance(properties[k], dict):
            convert_properties_obj_in_prop(properties=properties[k], property=property)


def resolve_mutation_tracker(mutation_tracker):
    body = {}
    for key in mutation_tracker:
        update_dictionary = body
        splitted = key.split('.')
        last_element = splitted[-1:][0]
        for attr in splitted:
            if attr == last_element:
                update_dictionary[attr] = mutation_tracker[key]
            else:
                if attr not in update_dictionary:
                    update_dictionary[attr] = {}
                update_dictionary = update_dictionary[attr]
    return body
