from datetime import datetime

from contacthub.models.customer_properties.base_property import BaseProperty


class Like(BaseProperty):
    DATE_PROPERTIES = {'createdTime': "%Y-%m-%d %I:%M"}

    def __getattr__(self, item):
        if item in self.DATE_PROPERTIES:
            return datetime.strptime(self.likes[item], self.DATE_PROPERTIES[item])
        return self.properties[item]