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

    __slots__ = ('internal_properties', 'parent_attr', 'mute', 'parent')

    def __init__(self, parent=None, parent_attr=None, **internal_properties):
        """
        :param json_properties: A dictionary with json_properties to return or set
        """
        self.parent_attr = parent_attr
        self.parent = parent
        self.mute = parent.mute if parent else None
        convert_properties_obj_in_prop(properties=internal_properties, property=Property)
        self.internal_properties = internal_properties

    @classmethod
    def from_dict(cls, parent=None, parent_attr=None, internal_properties=None):
        o = cls(parent=parent, parent_attr=parent_attr)
        if internal_properties is None:
            o.internal_properties = {}
        else:
            o.internal_properties = internal_properties
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
                return ReadOnlyList(list_item(self.SUBPROPERTIES_LIST[item], self.internal_properties[item]))
            if isinstance(self.internal_properties[item], dict):
                return Property.from_dict(parent_attr=self.parent_attr + '.' + item, parent=self,
                                        internal_properties=self.internal_properties[item])
            elif isinstance(self.internal_properties[item], list):
                if self.internal_properties[item] and isinstance(self.internal_properties[item][0], dict):
                    list_sub_prob = []
                    for elem in self.internal_properties[item]:
                        list_sub_prob.append(Property.from_dict(parent_attr=self.parent_attr + '.' + item, parent=self,
                                                              internal_properties=elem))
                else:
                    list_sub_prob = self.internal_properties[item]
                return ReadOnlyList(list_sub_prob)

            return self.internal_properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Property, self).__setattr__(attr, val)
        else:
            if isinstance(val, Property):
                try:
                    mutations = generate_mutation_tracker(self.internal_properties[attr], val.internal_properties)
                    update_tracking_with_new_prop(mutations, val.internal_properties)
                    self.mute[self.parent_attr + '.' + attr] = mutations
                except KeyError as e:
                    self.mute[attr] = val.internal_properties
                self.internal_properties[attr] = val.internal_properties
            else:
                self.internal_properties[attr] = val
                field = self.parent_attr.split('.')[-1:][0]
                if isinstance(self.parent.internal_properties[field], list):
                    self.mute[self.parent_attr] = self.parent.internal_properties[field]
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



