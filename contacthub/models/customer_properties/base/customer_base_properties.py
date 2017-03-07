from datetime import datetime

from contacthub.models.customer_properties.base.address import Address
from contacthub.models.customer_properties.base.contacts import Contacts
from contacthub.models.customer_properties.base.login_credentials import LoginCredentials
from contacthub.models.customer_properties.base.social_profile import SocialProfile

from contacthub.lib.utils import list_item
from contacthub.models.customer_properties.base.subscription import Subscription
from contacthub.models.customer_properties.property import Property
from contacthub.models.education import Education
from contacthub.models.job import Job
from contacthub.models.like import Like


class CustomerBaseProperties(Property):
    """
    Generic class for a Customer base property
    """
    SUBPROPERTIES_OBJ = {'contacts': Contacts, 'address': Address, 'credential': LoginCredentials, 'socialProfile': SocialProfile}
    SUBPROPERTIES_LIST = {'educations': Education, 'subscriptions': Subscription, 'likes': Like, 'jobs': Job}
    DATE_PROPERTIES = {'dob': "%Y-%m-%d"}

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        if item in self.SUBPROPERTIES_OBJ:
            if self.properties[item] is None:
                return None
            return self.SUBPROPERTIES_OBJ[item](self.properties[item])

        if item in self.DATE_PROPERTIES:
            return datetime.strptime(self.properties[item], self.DATE_PROPERTIES[item])

        if item in self.SUBPROPERTIES_LIST:
            return list_item(self.SUBPROPERTIES_LIST[item], self.properties[item])
        try:
            return self.properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))


