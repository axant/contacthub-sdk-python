# -*- coding: utf-8 -*-
from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager
from contacthub.models.query.query_builder import QueryBuilder


class Node(object):

    def __init__(self, workspace, node_id):
        self.workspace = workspace
        self.node_id = str(node_id)

    @property
    def customers(self):
        return CustomerDeclarativeApiManager(self).get_all()

    def query(self, entity):
        return QueryBuilder(self, entity)
