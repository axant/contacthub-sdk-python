from six import with_metaclass

from contacthub.DeclarativeAPIManager.declarative_api_event import EventDeclarativeApiManager
from contacthub.models.entity import Entity
from contacthub.models.query.entity_meta import EntityMeta
from contacthub.models.tags import Tags


class Customer(with_metaclass(EntityMeta, object)):
    """
    Customer model
    """
    __slots__ = ('json_properties', 'node')
    #DATE_PROPERTIES = {'registeredAt': '2017-03-14T15:36:16.245+0000', 'updatedAt'}

    def __init__(self, json_properties=None, node=None, **kwargs):
        """
        :param json_properties: A dictionary containing the json_properties related to customers
        """
        if json_properties is None:
            json_properties = dict()
            for k in kwargs:
                if isinstance(kwargs[k], Entity):
                    json_properties[k] = kwargs[k].json_properties
                else:
                    json_properties[k] = kwargs[k]

        self.json_properties = json_properties
        self.node = node

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        try:
            if isinstance(self.json_properties[item], dict):
                if item == 'tags':
                    return Tags(json_properties=self.json_properties[item])
                else:
                    return Entity(json_properties=self.json_properties[item])
            else:
                return self.json_properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" % (type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Customer, self).__setattr__(attr, val)
        else:
            if isinstance(val, Entity):
                self.json_properties[attr] = val.json_properties
            else:
                self.json_properties[attr] = val

    __metaclass__ = EntityMeta

    @property
    def events(self):
        """
        Get all the events in this node for a single customer specified
        :param id: the id of the customer for fetching the events associated
        :return: A list containing Events object of a node
        """
        if self.node and 'id' in self.json_properties:
            return EventDeclarativeApiManager(self.node).get_all(customer_id=self.json_properties['id'], read_only=True)
        raise Exception('Cannot retrieve events from a new customer.')