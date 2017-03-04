import json

from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager


class Query(object):

    def __init__(self, node, criterion):
        self.node = node
        self.criterion = criterion

    def all(self):
        return CustomerDeclarativeApiManager(self.node).get_all(query=self.criterion)


