from datetime import datetime

from contacthub.lib.utils import list_item
from contacthub.models.education import Education
from contacthub.models.job import Job
from contacthub.models.like import Like


class Entity(object):
    """
    Generic property for all entities
    """

    SUBPROPERTIES_LIST = {'educations': Education, 'likes': Like, 'jobs': Job}

    __slots__ = ('json_properties', 'father', 'mute', 'father_class')

    def __init__(self, json_properties=None, mute=None, father=None, father_class=None, *args, **kwargs):
        """
        :param json_properties: A dictionary with json_properties to return or set
        """
        if json_properties is None:
            json_properties = dict()
            for k in kwargs:
                if isinstance(kwargs[k], Entity):
                    json_properties[k] = kwargs[k].json_properties
                else:
                    json_properties[k] = kwargs[k]
        self.json_properties = json_properties
        self.father = father
        self.mute = mute
        self.father_class = father_class

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        try:
            if item in self.SUBPROPERTIES_LIST:
                return list_item(self.SUBPROPERTIES_LIST[item], self.json_properties[item])
            if isinstance(self.json_properties[item], dict):
                return Entity(self.json_properties[item], mute=self.mute, father=self.father + '.' + item, father_class=self)
            elif isinstance(self.json_properties[item], list):
                list_sub_prob = []
                for elem in self.json_properties[item]:
                    list_sub_prob.append(Entity(elem, mute=self.mute, father=self.father + '.' + item, father_class=self))
                return list_sub_prob
            return self.json_properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Entity, self).__setattr__(attr, val)
        else:
            if isinstance(val, Entity):
                raise Exception("Operation not permitted: cannot assign an Entity object to an attribute")
            else:
                self.json_properties[attr] = val
                field = self.father.split('.')[-1:][0]
                if isinstance(self.father_class.json_properties[field], list):
                    self.mute[self.father] = self.father_class.json_properties[field]
                else:
                    self.mute[self.father + '.' + attr] = val


