from contacthub.models.customer_base_properties import CustomerBaseProperties
from contacthub.models.entity import Entity
from contacthub.models.tags import Tags


class Customer(object):
    __slots__ = ('customer_properties',)
    SUBPROPERTIES = {'base': CustomerBaseProperties, 'tags': Tags}

    def __init__(self, customer_properties):
        self.customer_properties = customer_properties

    def __getattr__(self, item):
        if item in self.SUBPROPERTIES:
            if self.customer_properties[item] is None:
                return None
            return self.SUBPROPERTIES[item](self.customer_properties[item])
        else:
            return self.customer_properties[item]

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Customer, self).__setattr__(attr, val)
        else:
            self.customer_properties[attr] = val

    __metaclass__ = Entity
