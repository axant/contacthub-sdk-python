from contacthub.models.customer_properties.base.customer_base_properties import CustomerBaseProperties
from contacthub.models.customer_properties.tags import Tags
from contacthub.models.query.entity_meta import EntityMeta


class Customer(object, metaclass=EntityMeta):
    """
    Customer model
    """
    __slots__ = ('customer_properties',)
    SUBPROPERTIES = {'base': CustomerBaseProperties, 'tags': Tags}

    def __init__(self, customer_properties):
        """
        :param customer_properties: A dictionary containing the properties related to customers
        """
        self.customer_properties = customer_properties

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        if item in self.SUBPROPERTIES:
            return self.SUBPROPERTIES[item](self.customer_properties[item])
        else:
            try:
                return self.customer_properties[item]
            except KeyError as e:
                raise AttributeError("%s object has no attribute %s" % (type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Customer, self).__setattr__(attr, val)
        else:
            self.customer_properties[attr] = val

    __metaclass__ = EntityMeta
