from contacthub.lib.utils import list_item
from contacthub.models.base_property import BaseProperty


class MobileDevice(BaseProperty):

    class TYPES:
        IOS = 'IOS'
        GCM = 'GCM'
        WP = 'WP'


class OtherContact(BaseProperty):

    class TYPES:
        MOBILE = 'MOBILE'
        PHONE = 'PHONE'
        EMAIL = 'EMAIL'
        FAX = 'FAX'
        OTHER = 'OTHER'


class Contacts(BaseProperty):
    SUBPROPERTIES_LIST = {'otherContacts': OtherContact, 'mobileDevices': MobileDevice}

    def __getattr__(self, item):
        if self.properties[item] is None:
            return None

        if item in self.SUBPROPERTIES_LIST:
            return list_item(self.SUBPROPERTIES_LIST[item], self.properties[item])
        else:
            return self.properties[item]
