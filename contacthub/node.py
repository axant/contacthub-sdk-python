# -*- coding: utf-8 -*-
from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager
from contacthub.DeclarativeAPIManager.declarative_api_event import EventDeclarativeApiManager
from contacthub.models.customer import Customer
from contacthub.models.query.query import Query


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
        self.customer_api_manager = CustomerDeclarativeApiManager(node=self, entity=Customer)

    def get_customers(self, externalId=None, page=None, size=None):
        """
        Get all the customers in this node
        :return: A list containing Customer object of a node
        """
        return self.customer_api_manager.get_all(externalId=externalId, page=page, size=size)

    def get_customer(self, id=None, externalId=None):
        return self.customer_api_manager.get(id=id, externalId=externalId)

    def query(self, entity):
        """
        Create a QueryBuilder object for a given entity, that allows to filter the entity's data
        :param entity: A class of model on which to run the query
        :return: A QueryBuilder object for the specified entity
        """
        return Query(node=self, entity=entity)

    def delete_customer(self, customer):
        return self.customer_api_manager.delete(customer=customer)

    def add_customer(self, customer, force_update=False):
        return self.customer_api_manager.post(customer=customer, force_update=force_update)

    def update_customer(self, customer, full_update=False):
        if full_update:
            return self.customer_api_manager.put(customer=customer)
        else:
            return self.customer_api_manager.patch(customer=customer)


