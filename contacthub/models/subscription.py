from datetime import datetime

from contacthub.lib.utils import list_item
from contacthub.models.base_property import BaseProperty


class Preference(BaseProperty):
    pass


class Subscription(BaseProperty):

    class KINDS:
        DIGITAL_MESSAGE = 'DIGITAL_MESSAGE'
        SERVICE = 'SERVICE'
        OTHER = 'OTHER'

    SUBPROPERTIES_LIST = {'preferences': Preference}
    SUBPROPERTIES_DATE = {'startDate': "%Y-%m-%d", 'endDate': "%Y-%m-%d", 'registeredAt': "%Y-%m-%d", 'updatedAt': "%Y-%m-%d" }

    def __getattr__(self, item):
        if item in self.SUBPROPERTIES_LIST:
            return list_item(self.SUBPROPERTIES_LIST[item], self.properties[item])

        if item in self.SUBPROPERTIES_DATE:
            return datetime.strptime(self.properties[item], self.SUBPROPERTIES_DATE[item])

        return self.properties[item]