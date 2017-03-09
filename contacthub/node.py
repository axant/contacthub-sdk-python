# -*- coding: utf-8 -*-
from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager
from contacthub.DeclarativeAPIManager.declarative_api_event import EventDeclarativeApiManager
from contacthub.models.customer import Customer
from contacthub.models.query.query_builder import QueryBuilder


class Node(object):
    """
    Node class for accessing data on a ContactHub node.
    """
    def __init__(self, workspace, node_id):
        """
        :param workspace: A Workspace Object for authenticating on ContactHub
        :param node_id: The id of the ContactHub node
        """
        self.workspace = workspace
        self.node_id = str(node_id)

    @property
    def customers(self):
        """
        Get all the customers in this node
        :return: A list containing Customer object of a node
        """
        return CustomerDeclarativeApiManager(self).get_all()


    def query(self, entity):
        """
        Create a QueryBuilder object for a given entity, that allows to filter the entity's data
        :param entity: A class of model on which to run the query
        :return: A QueryBuilder object for the specified entity
        """
        return QueryBuilder(self, entity)

    def post(self, entity):
        """
        Post a new specified entity in contactHub APIs
        :param entity: a model's object to post
        :return: a
        """
        if isinstance(entity, Customer):
            return CustomerDeclarativeApiManager(self).post(entity)