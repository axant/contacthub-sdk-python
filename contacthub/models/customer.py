from copy import deepcopy

from contacthub.api_manager.api_customer import CustomerAPIManager
from contacthub.api_manager.api_event import EventAPIManager
from contacthub.lib.read_only_list import ReadOnlyList
from contacthub.lib.utils import generate_mutation_tracker, convert_properties_obj_in_prop, \
    resolve_mutation_tracker
from contacthub.models.event import Event
from six import with_metaclass

from contacthub.models.properties import Properties
from contacthub.models.query.entity_meta import EntityMeta


class Customer(with_metaclass(EntityMeta, object)):
    """
    Customer model
    """
    __slots__ = ('attributes', 'node', 'customer_api_manager', 'event_api_manager', 'mute')

    def __init__(self, node, default_props=None, **attributes):
        """
        :param json_properties: A dictionary containing the json_properties related to customers
        """

        convert_properties_obj_in_prop(properties=attributes, properties_class=Properties)
        if default_props is None:
            if 'base' not in attributes:
                attributes['base'] = {}

            if 'contacts' not in attributes['base']:
                attributes['base']['contacts'] = {}

            if 'extended' not in attributes or attributes['extended'] is None:
                attributes['extended'] = {}

            if 'tags' not in attributes or attributes['tags'] is None:
                attributes['tags'] = {'auto': [], 'manual': []}
            self.attributes = attributes
        else:
            default_props.update(attributes)
            self.attributes = default_props

        self.node = node
        self.customer_api_manager = CustomerAPIManager(node=self.node)
        self.event_api_manager = EventAPIManager(node=self.node)
        self.mute = {}

    @classmethod
    def from_dict(cls, node, attributes=None):
        o = cls(node=node)
        if attributes is None:
            o.attributes = {}
        else:
            o.attributes = attributes
        return o

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple properties. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base properties dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        try:
            if isinstance(self.attributes[item], dict):
                return Properties.from_dict(parent_attr=item, parent=self, attributes=self.attributes[item])
            else:
                return self.attributes[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" % (type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Customer, self).__setattr__(attr, val)
        else:
            if isinstance(val, Properties):
                try:
                    tracker = generate_mutation_tracker(self.attributes[attr], val.attributes)
                    for key in val.attributes:
                        if key not in tracker or (key in tracker and val.attributes[key]):
                            tracker[key] = val.attributes[key]
                    self.mute[attr] = tracker
                except KeyError as e:
                    self.mute[attr] = val.attributes
                self.attributes[attr] = val.attributes
            else:
                self.attributes[attr] = val
                self.mute[attr] = val

    __metaclass__ = EntityMeta

    @property
    def events(self):
        """
        Get all the events in this node for a single customer specified
        :param id: the id of the customer for fetching the events associated
        :return: A list containing Events object of a node
        """
        if self.node and 'id' in self.attributes:
            events = []
            resp = self.event_api_manager.get_all(customer_id=self.attributes['id'])
            for event in resp['elements']:
                events.append(Event.from_dict(node=self.node, attributes=event))
            return ReadOnlyList(events)
        raise Exception('Cannot retrieve events from a new customer created.')

    def post(self, force_update=False):
        self.customer_api_manager.post(body=self.attributes, force_update=force_update)

    def delete(self):
        self.customer_api_manager.delete(_id=self.attributes['id'])

    def patch(self):
        tracker = resolve_mutation_tracker(self.mute)
        self.customer_api_manager.patch(_id=self.attributes['id'], body=tracker)

    def put(self):
        body = deepcopy(self.attributes)
        body.pop('registeredAt', None)
        body.pop('updatedAt', None)
        if 'base' in body and 'timezone' in body['base'] and body['base']['timezone'] is None:
            body['base']['timezone'] = 'Europe/Rome'
        self.customer_api_manager.put(_id=self.attributes['id'], body=body)

    def mutation_tracker(self):
        return resolve_mutation_tracker(self.mute)

    def to_dict(self):
        return deepcopy(self.attributes)
