
from six import with_metaclass

from contacthub.DeclarativeAPIManager.declarative_api_event import EventDeclarativeApiManager
from contacthub.models.entity import Entity
from contacthub.models.query.entity_meta import EntityMeta
from contacthub.models.tags import Tags
from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager


class Customer(with_metaclass(EntityMeta, object)):
    """
    Customer model
    """
    __slots__ = ('json_properties', 'node', 'customer_api_manager', 'event_api_manager', 'mute')

    def __init__(self, node, json_properties=None, **kwargs):
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
        if 'extended' not in self.json_properties or self.json_properties['extended'] is None:
            self.json_properties['extended'] = {}
        if 'tags' not in self.json_properties or self.json_properties['tags'] is None:
            self.json_properties['tags'] = {'auto': [], 'manual': []}

        self.node = node
        self.customer_api_manager = CustomerDeclarativeApiManager(node=self.node, entity=Customer)
        self.event_api_manager = EventDeclarativeApiManager(node=self.node)

        self.mute = {}

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        try:
            if item == 'tags':
                return Tags(json_properties=self.json_properties[item])
            if item == 'extended':
                return self.json_properties['extended']
            if isinstance(self.json_properties[item], dict):
                return Entity(self.json_properties[item], mute=self.mute, father=item, father_class=self)
            else:
                return self.json_properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" % (type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Customer, self).__setattr__(attr, val)
        else:
            if isinstance(val, Entity):
                raise Exception("Operation not permitted: cannot assign an Entity object to an attribute")
            else:
                self.json_properties[attr] = val
                self.mute[attr] = val

    __metaclass__ = EntityMeta

    @property
    def events(self):
        """
        Get all the events in this node for a single customer specified
        :param id: the id of the customer for fetching the events associated
        :return: A list containing Events object of a node
        """
        if self.node and 'id' in self.json_properties:
            return self.event_api_manager.get_all(customer_id=self.json_properties['id'], read_only=True)
        raise Exception('Cannot retrieve events from a new customer created.')

    def post(self, force_update=False):
        return self.customer_api_manager.post(self, force_update=force_update)

    def delete(self):
        if self.node and 'id' in self.json_properties:
            return self.customer_api_manager.delete(self)
        raise Exception('Cannot delete a new customer created.')

    def patch(self):
        return self.customer_api_manager.patch(self)

    def put(self):
        return self.customer_api_manager.put(self)
