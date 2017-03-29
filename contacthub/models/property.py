from datetime import datetime

from contacthub.lib.read_only_list import ReadOnlyList
from contacthub.lib.utils import list_item, get_dictionary_paths, generate_mutation_tracker, convert_properties_obj_in_prop
from contacthub.models.education import Education
from contacthub.models.job import Job
from contacthub.models.like import Like
from copy import deepcopy


class Property(object):
    """
    Generic property for all entities
    """

    SUBPROPERTIES_LIST = {'educations': Education, 'likes': Like, 'jobs': Job}

    __slots__ = ('attributes', 'parent_attr', 'mute', 'parent')

    def __init__(self, parent=None, parent_attr=None, **attributes):
        """
        :param json_properties: A dictionary with json_properties to return or set
        """
        self.parent_attr = parent_attr
        self.parent = parent
        self.mute = parent.mute if parent else None
        convert_properties_obj_in_prop(properties=attributes, property=Property)
        self.attributes = attributes

    @classmethod
    def from_dict(cls, parent=None, parent_attr=None, attributes=None):
        o = cls(parent=parent, parent_attr=parent_attr)
        if attributes is None:
            o.attributes = {}
        else:
            o.attributes = attributes
        return o

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or
        a list
        """
        try:
            if item in self.SUBPROPERTIES_LIST:
                obj_list_ret = []
                for elements in self.attributes[item]:
                    obj_list_ret.append(self.SUBPROPERTIES_LIST[item](customer=self.parent, **elements))
                return ReadOnlyList(obj_list_ret)
            if isinstance(self.attributes[item], dict):
                return Property.from_dict(parent_attr=self.parent_attr + '.' + item, parent=self,
                                        attributes=self.attributes[item])
            elif isinstance(self.attributes[item], list):
                if self.attributes[item] and isinstance(self.attributes[item][0], dict):
                    list_sub_prob = []
                    for elem in self.attributes[item]:
                        list_sub_prob.append(Property.from_dict(parent_attr=self.parent_attr + '.' + item, parent=self,
                                                              attributes=elem))
                else:
                    list_sub_prob = self.attributes[item]
                return ReadOnlyList(list_sub_prob)

            return self.attributes[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Property, self).__setattr__(attr, val)
        else:
            if isinstance(val, Property):
                try:
                    mutations = generate_mutation_tracker(self.attributes[attr], val.attributes)
                    update_tracking_with_new_prop(mutations, val.attributes)
                    self.mute[self.parent_attr + '.' + attr] = mutations
                except KeyError as e:
                    self.mute[attr] = val.attributes
                self.attributes[attr] = val.attributes
            else:
                self.attributes[attr] = val
                field = self.parent_attr.split('.')[-1:][0]
                if isinstance(self.parent.attributes[field], list):
                    self.mute[self.parent_attr] = self.parent.attributes[field]
                else:
                    self.mute[self.parent_attr + '.' + attr] = val


def update_tracking_with_new_prop(mutations, new_properties):
    """

    :param old_props:
    :param new_props:
    """
    for key in new_properties:
        if (key not in mutations or mutations[key] is None or not mutations[key]) and \
                not isinstance(new_properties[key], dict):
            mutations[key] = new_properties[key]
        elif isinstance(new_properties[key], dict):
            mutations[key] = {}
            update_tracking_with_new_prop(mutations[key], new_properties[key])



