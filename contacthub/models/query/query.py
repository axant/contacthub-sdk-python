import json

from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager


class Query(object):

    def __init__(self, node, query):
        self.node = node
        self.query = json.dumps(query)

    def all(self):
        return CustomerDeclarativeApiManager(self.node).get_all(query=self.query)


