from copy import deepcopy

from contacthub.lib.utils import get_dictionary_paths, generate_mutation_tracker
from six import with_metaclass

from contacthub.DeclarativeAPIManager.declarative_api_event import EventDeclarativeApiManager
from contacthub.models.entity import Entity
from contacthub.models.query.entity_meta import EntityMeta
from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager


class Customer(with_metaclass(EntityMeta, object)):
    """
    Customer model
    """
    __slots__ = ('properties', 'node', 'customer_api_manager', 'event_api_manager', 'mute')

    def __init__(self, node, **properties):
        """
        :param json_properties: A dictionary containing the json_properties related to customers
        """
        for k in properties:
            if isinstance(properties[k], Entity):
                properties[k] = properties[k].properties
            else:
                properties[k] = properties[k]

        self.properties = properties
        if 'extended' not in self.properties or self.properties['extended'] is None:
            self.properties['extended'] = {}
        if 'tags' not in self.properties or self.properties['tags'] is None:
            self.properties['tags'] = {'auto': [], 'manual': []}

        self.node = node
        self.customer_api_manager = CustomerDeclarativeApiManager(node=self.node, entity=Customer)
        self.event_api_manager = EventDeclarativeApiManager(node=self.node)
        self.mute = {}

    @classmethod
    def from_dict(cls, node, properties=None):
        o = cls(node=node, **properties)
        o.properties = properties or {}
        return o

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        try:
            if isinstance(self.properties[item], dict):
                return Entity.from_dict(parent_attr=item, parent=self, properties=self.properties[item])
            else:
                return self.properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" % (type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Customer, self).__setattr__(attr, val)
        else:
            if isinstance(val, Entity):
                    # main_list_of_paths = []
                    # tmp_list_for_path = []
                    #
                    # get_dictionary_paths(self.json_properties[attr], main_list=main_list_of_paths,
                    #                      tmp_list=tmp_list_for_path)
                    # #  we start wih the whole old dictionary, next we will set the missing keys to None
                    # mutation_tracker = deepcopy(self.json_properties[attr])
                    # #  follow the paths for searching keys not in new properties but in the old ones (mutation_tracker)
                    #
                    # for key_paths in main_list_of_paths:
                    #     new_properties = val.json_properties
                    #     actual_mutation_tracker = mutation_tracker
                    #     for single_key in key_paths:
                    #         if single_key not in new_properties or not new_properties[single_key]:
                    #             actual_mutation_tracker[single_key] = None
                    #             break
                    #         else:
                    #             actual_mutation_tracker[single_key] = new_properties[single_key]
                    #             new_properties = new_properties[single_key]
                    #             actual_mutation_tracker = actual_mutation_tracker[single_key]
                tracker = generate_mutation_tracker(self.properties[attr], val.properties)
                for key in val.properties:
                    if key not in tracker or (key in tracker and val.properties[key]):
                        tracker[key] = val.properties[key]
                self.mute[attr] = tracker
                self.properties[attr] = val.properties
            else:
                self.properties[attr] = val
                self.mute[attr] = val

    __metaclass__ = EntityMeta


    @property
    def events(self):
        """
        Get all the events in this node for a single customer specified
        :param id: the id of the customer for fetching the events associated
        :return: A list containing Events object of a node
        """
        if self.node and 'id' in self.properties:
            return self.event_api_manager.get_all(customer_id=self.properties['id'], read_only=True)
        raise Exception('Cannot retrieve events from a new customer created.')

    def post(self, force_update=False):
        return self.customer_api_manager.post(self, force_update=force_update)

    def delete(self):
        if self.node and 'id' in self.properties:
            return self.customer_api_manager.delete(self)
        raise Exception('Cannot delete a new customer created.')

    def patch(self):
        return self.customer_api_manager.patch(self)

    def put(self):
        return self.customer_api_manager.put(self)
