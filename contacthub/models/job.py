from datetime import datetime
from contacthub.models.base_property import BaseProperty


class Job(BaseProperty):

    DATE_PROPERTIES = {'startDate': "%Y-%m-%d", 'endDate': "%Y-%m-%d"}

    def __getattr__(self, item):
        if item in self.DATE_PROPERTIES:
            return datetime.strptime(self.properties[item], self.DATE_PROPERTIES[item])
        return self.properties[item]
