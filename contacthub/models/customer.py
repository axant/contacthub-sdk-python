# -*- coding: utf-8 -*-
from copy import deepcopy

from contacthub._api_manager._api_customer import _CustomerAPIManager
from contacthub._api_manager._api_event import _EventAPIManager
from contacthub.errors.operation_not_permitted import OperationNotPermitted
from contacthub.lib.read_only_list import ReadOnlyList
from contacthub.lib.utils import generate_mutation_tracker, convert_properties_obj_in_prop, \
    resolve_mutation_tracker, remove_empty_attributes
from contacthub.models.event import Event
from six import with_metaclass

from contacthub.models.properties import Properties
from contacthub.models.query.entity_meta import EntityMeta


class Customer(with_metaclass(EntityMeta, object)):
    """
    Customer entity definition
    """
    __attributes__ = ('attributes', 'node', 'customer_api_manager', 'event_api_manager', 'mute')

    def __init__(self, node, default_attributes=None, **attributes):
        """
        Initialize a customer in a node with the specified attributes.

        :param node: the node of the customer
        :param default_attributes: the attributes schema. By default is the following dictionary:
            {
            'base':
                    {
                    'contacts': {}
                    },
            'extended': {},
            'tags': {
                    'manual': [],
                    'auto': []
                    }
            }
        :param attributes: key-value arguments for generating the structure of Customer's attributes
        """

        convert_properties_obj_in_prop(properties=attributes, properties_class=Properties)
        if default_attributes is None:
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
            default_attributes.update(attributes)
            self.attributes = default_attributes

        self.node = node
        self.customer_api_manager = _CustomerAPIManager(node=self.node)
        self.event_api_manager = _EventAPIManager(node=self.node)
        self.mute = {}

    @classmethod
    def from_dict(cls, node, attributes=None):
        """
        Create a new Customer initialized by a specified dictionary of attributes

        :rtype: Customer
        :param node: the node of the customer
        :param attributes: a dictionary representing the attributes of the new Customer
        :return: a new Customer object
        """
        o = cls(node=node)
        if attributes is None:
            o.attributes = {}
        else:
            o.attributes = attributes
        return o

    def to_dict(self):
        """
        Convert this Customer in a dictionary containing his attributes.

        :rtype: dict
        :return: a new dictionary representing the attributes of this Customer
        """
        return deepcopy(self.attributes)

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple attribute. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.

        :param item: the key of the base properties dict
        :return: the item in the attributes dictionary if it's present, raise AttributeError otherwise.
        """
        try:
            if isinstance(self.attributes[item], dict):
                return Properties.from_dict(parent_attr=item, parent=self, attributes=self.attributes[item])
            else:
                return self.attributes[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" % (type(self).__name__, e))

    def __setattr__(self, attr, val):
        """
        x.__setattr__('attr', val) <==> x.attr = val
        If `val` is simple type value (dictionary, list, str, int, ecc.), update the attributes dictionary with new
        values, otherwise, if `val` is instance of Properties, check for mutations in the Properties object.
        This method generate the mutation tracker dictionary.
        """
        if attr in self.__attributes__:
            return super(Customer, self).__setattr__(attr, val)
        else:
            if isinstance(val, Properties):
                try:
                    tracker = generate_mutation_tracker(self.attributes[attr], val.attributes)
                    for key in val.attributes:
                        if key not in tracker or (key in tracker and val.attributes[key]):
                            tracker[key] = val.attributes[key]
                    self.mute[attr] = tracker
                except KeyError:
                    self.mute[attr] = val.attributes
                self.attributes[attr] = val.attributes
            else:
                self.attributes[attr] = val
                self.mute[attr] = val

    __metaclass__ = EntityMeta

    @property
    def events(self):
        """
        Get all the events associated to this Customer.

        :rtype: list
        :return: A list containing Events object associated to this Customer
        """
        if self.node and 'id' in self.attributes:
            events = []
            resp = self.event_api_manager.get_all(customer_id=self.attributes['id'])
            for event in resp['elements']:
                events.append(Event.from_dict(node=self.node, attributes=event))
            return ReadOnlyList(events)
        raise OperationNotPermitted('Cannot retrieve events from a new customer created.')

    def post(self, force_update=False):
        """
        Post this Customer in the associated Node.

        :param force_update: if it's True and the customer already exists in the node, patch the customer with the
                             modified properties.
        """
        self.attributes.pop('registeredAt', None)
        self.attributes.pop('updatedAt', None)
        self.attributes.pop('id', None)
        body = remove_empty_attributes(self.attributes)
        self.customer_api_manager.post(body=body, force_update=force_update)

    def delete(self):
        """
        Delete this customer from the associated Node.
        """
        self.customer_api_manager.delete(_id=self.attributes['id'])

    def patch(self):
        """
        Patch this customer in the associated node, updating his attributes with the modified ones.
        """
        tracker = resolve_mutation_tracker(self.mute)
        self.customer_api_manager.patch(_id=self.attributes['id'], body=tracker)

    def put(self):
        """
        Put this customer in the associated node, substituting all the old attributes with the ones in this Customer.
        """
        body = deepcopy(self.attributes)
        body.pop('registeredAt', None)
        body.pop('updatedAt', None)
        if 'base' in body and 'timezone' in body['base'] and body['base']['timezone'] is None:
            body['base']['timezone'] = 'Europe/Rome'
        self.customer_api_manager.put(_id=self.attributes['id'], body=body)

    def get_mutation_tracker(self):
        """
        Get the mutation tracker for this customer

        :rtype: dict
        :return: the mutation tracker of this customer
        """
        return resolve_mutation_tracker(self.mute)

    class OTHER_CONTACT_TYPES:
        MOBILE = 'MOBILE'
        PHONE = 'PHONE'
        EMAIL = 'EMAIL'
        FAX = 'FAX'
        OTHER = 'OTHER'

    class MOBILE_DEVICE_TYPES:
        APN = 'APN'
        GCM = 'GCM'
        WP = 'WP'

    class NOTIFICATION_SERVICES:
        APN = "APN"
        GCM = "GCM"
        WNS = "WNS"
        ADM = "ADM"
        SNS = "SNS"
