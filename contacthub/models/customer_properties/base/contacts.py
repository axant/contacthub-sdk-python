from contacthub.lib.utils import list_item
from contacthub.models.customer_properties.property import Property


class MobileDevice(Property):
    """
    MobileDevice sub property of the Contacts property
    """

    class TYPES:
        """
        Subclasses with MobileDevice types for the type field of a MobileDevice
        """
        IOS = 'IOS'
        GCM = 'GCM'
        WP = 'WP'


class OtherContact(Property):
    """
    OtherContact sub property of the Contacts property
    """

    class TYPES:
        """
        Subclasses with OtherContact types for the type field of a OtherContact
        """
        MOBILE = 'MOBILE'
        PHONE = 'PHONE'
        EMAIL = 'EMAIL'
        FAX = 'FAX'
        OTHER = 'OTHER'


class Contacts(Property):
    """
    Login Credential sub property of CustomerBaseProperties
    """
    SUBPROPERTIES_LIST = {'otherContacts': OtherContact, 'mobileDevices': MobileDevice}

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """

        if item in self.SUBPROPERTIES_LIST:
            return list_item(self.SUBPROPERTIES_LIST[item], self.properties[item])
        try:
            return self.properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" % (type(self).__name__, e))
