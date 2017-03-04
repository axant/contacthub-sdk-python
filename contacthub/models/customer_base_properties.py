from datetime import datetime
from contacthub.lib.utils import list_item
from contacthub.models.address import Address
from contacthub.models.contacts import Contacts
from contacthub.models.education import Education
from contacthub.models.job import Job
from contacthub.models.like import Like
from contacthub.models.login_credentials import LoginCredentials
from contacthub.models.social_profile import SocialProfile
from contacthub.models.subscription import Subscription


class CustomerBaseProperties(object):
    SUBPROPERTIES_OBJ = {'contacts': Contacts, 'address': Address, 'credential': LoginCredentials, 'socialProfile': SocialProfile}
    SUBPROPERTIES_LIST = {'educations': Education, 'subscriptions': Subscription, 'likes': Like, 'jobs': Job}
    DATE_PROPERTIES = {'dob': "%Y-%m-%d"}

    def __init__(self, base_properties):
        self.base_properties = base_properties

    def __getattr__(self, item):

        if item in self.SUBPROPERTIES_OBJ:
            if self.base_properties[item] is None:
                return None
            return self.SUBPROPERTIES_OBJ[item](self.base_properties[item])

        if item in self.DATE_PROPERTIES:
            return datetime.strptime(self.base_properties[item], self.DATE_PROPERTIES[item])

        if item in self.SUBPROPERTIES_LIST:
            return list_item(self.SUBPROPERTIES_LIST[item], self.base_properties[item])

        return self.base_properties[item]


