from datetime import datetime

from contacthub.lib.utils import list_item
from contacthub.models.education import Education
from contacthub.models.job import Job
from contacthub.models.like import Like


class Entity(object):
    """
    Generic property for all entities
    """
    SUBPROPERTIES_OBJ = ['contacts', 'address',  'credential', 'socialProfile', 'geo']
    SUBPROPERTIES_LIST = {'educations': Education, 'likes': Like, 'jobs': Job}
    SUBPROPERTIES_LIST_PROP = ['subscriptions', 'preferences', 'otherContacts', 'mobileDevices']
    DATE_PROPERTIES = {'dob': "%Y-%m-%d",'startDate': "%Y-%m-%d", 'endDate': "%Y-%m-%d", 'registeredAt': "%Y-%m-%d",
                       'updatedAt': "%Y-%m-%d", 'createdTime': "%Y-%m-%d %H:%M"}

    __slots__ = ('json_properties', )

    def __init__(self, json_properties=None, *args, **kwargs):
        """
        :param json_properties: A dictionary with json_properties to return or set
        """
        if json_properties is None:
            json_properties = dict()
            for k in kwargs:
                json_properties[k]=kwargs[k]

        self.json_properties = json_properties

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """

        if item in self.SUBPROPERTIES_OBJ:
            try:
                if self.json_properties[item] is None:
                    return None
                return Entity(self.json_properties[item])
            except KeyError as e:
                self.json_properties[item] = {}
                return Entity(self.json_properties[item])

        if item in self.SUBPROPERTIES_LIST:
            return list_item(self.SUBPROPERTIES_LIST[item], self.json_properties[item])

        if item in self.SUBPROPERTIES_LIST_PROP:
            return list_item(self.__class__, self.json_properties[item])

        if item in self.DATE_PROPERTIES:
            return datetime.strptime(self.json_properties[item], self.DATE_PROPERTIES[item])
        try:
            return self.json_properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Entity, self).__setattr__(attr, val)
        else:
            if isinstance(val, Entity):
                self.json_properties[attr] = val.json_properties
            else:
                self.json_properties[attr] = val
