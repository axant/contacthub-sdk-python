from datetime import datetime

from contacthub.lib.utils import list_item
from contacthub.models.customer_properties.property import Property


class Preference(Property):
    """
    Preference sub property of the Subscription property
    """
    pass


class Subscription(Property):
    """
    Subscription sub property of the CustomerBaseProperties
    """

    class KINDS:
        """
        Subclasses with subscription types for the kind field of a Subscription
        """
        DIGITAL_MESSAGE = 'DIGITAL_MESSAGE'
        SERVICE = 'SERVICE'
        OTHER = 'OTHER'

    SUBPROPERTIES_LIST = {'preferences': Preference}
    SUBPROPERTIES_DATE = {'startDate': "%Y-%m-%d", 'endDate': "%Y-%m-%d", 'registeredAt': "%Y-%m-%d", 'updatedAt': "%Y-%m-%d" }

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        if item in self.SUBPROPERTIES_LIST:
            return list_item(self.SUBPROPERTIES_LIST[item], self.properties[item])

        if item in self.SUBPROPERTIES_DATE:
            return datetime.strptime(self.properties[item], self.SUBPROPERTIES_DATE[item])
        try:
            return self.properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))