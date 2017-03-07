import json

from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager
from contacthub.models.query.entity_meta import EntityMeta


class Query(object):
    """
    Query object for applying the specified query in the APIs.

    Use this class for interact with the DeclarativeAPIManager Layer or APIManagerLevel and return the queried as object or
    json format variables
    """
    def __init__(self, node, query, entity):
        """
        :param node: the node for applying for fetching data
        :param query: a JSON API-like object for querying data
        :param entity: the entity on which apply the query
        """
        self.node = node
        self.query = query
        self.entity = entity

    def all(self):
        """
        Get all queried data of an entity from the API
        :return: a list of Entity object
        """
        if self.entity.__name__ == 'Customer':
            return CustomerDeclarativeApiManager(self.node).get_all(query=self.query)


