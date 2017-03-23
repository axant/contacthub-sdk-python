from datetime import datetime

from contacthub.lib.utils import list_item, get_dictionary_paths, generate_mutation_tracker
from contacthub.models.education import Education
from contacthub.models.job import Job
from contacthub.models.like import Like
from copy import deepcopy


class Entity(object):
    """
    Generic property for all entities
    """

    SUBPROPERTIES_LIST = {'educations': Education, 'likes': Like, 'jobs': Job}

    __slots__ = ('properties', 'parent_attr', 'mute', 'parent')

    def __init__(self, parent=None, parent_attr=None, **properties):
        """
        :param json_properties: A dictionary with json_properties to return or set
        """
        self.parent_attr = parent_attr
        self.parent = parent
        self.mute = parent.mute if parent else None
        for k in properties:
            if isinstance(properties[k], Entity):
                properties[k] = properties[k].properties
        self.properties = properties

    @classmethod
    def from_dict(cls, parent=None, parent_attr=None, properties=None):
        o = cls(parent=parent, parent_attr=parent_attr)
        for k in properties:
            if isinstance(properties[k], Entity):
                properties[k] = properties[k].properties
        if properties is None:
            o.properties = {}
        else:
            o.properties = properties
        return o

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        try:
            if item in self.SUBPROPERTIES_LIST:
                return list_item(self.SUBPROPERTIES_LIST[item], self.properties[item])
            if isinstance(self.properties[item], dict):
                return Entity.from_dict(parent_attr=self.parent_attr + '.' + item, parent=self,
                                        properties=self.properties[item])
            elif isinstance(self.properties[item], list) and self.properties[item] \
                    and isinstance(self.properties[item][0], dict):
                list_sub_prob = []
                for elem in self.properties[item]:
                    list_sub_prob.append(Entity.from_dict(parent_attr=self.parent_attr + '.' + item,
                                                          parent=self, properties=elem))
                return list_sub_prob
            return self.properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Entity, self).__setattr__(attr, val)
        else:
            if isinstance(val, Entity):
                mutations = generate_mutation_tracker(self.properties[attr], val.properties)
                update_tracking_with_new_prop(mutations, val.properties)
                self.mute[self.parent_attr + '.' + attr] = mutations
                self.properties[attr] = val.properties
            else:
                print (self.properties)
                self.properties[attr] = val
                field = self.parent_attr.split('.')[-1:][0]
                if isinstance(self.parent.properties[field], list):
                    self.mute[self.parent_attr] = self.parent.properties[field]
                else:
                    self.mute[self.parent_attr + '.' + attr] = val


def update_tracking_with_new_prop(mutations, new_properties):
    """

    :param old_props:
    :param new_props:
    """
    for key in new_properties:
        if (key not in mutations or mutations[key] is None or not mutations[key]) and not isinstance(new_properties[key],
                                                                                                     dict):
            mutations[key] = new_properties[key]
        elif isinstance(new_properties[key], dict):
            mutations[key] = {}
            update_tracking_with_new_prop(mutations[key], new_properties[key])



