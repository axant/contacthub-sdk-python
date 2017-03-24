# -*- coding: utf-8 -*-
from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager
from contacthub.DeclarativeAPIManager.declarative_api_event import EventDeclarativeApiManager
from contacthub.DeclarativeAPIManager.declarative_api_session import SessionDeclarativeAPIManager
from contacthub.models.customer import Customer
from contacthub.models.query.query import Query
import uuid


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
        self.session_api_manager = SessionDeclarativeAPIManager(node=self)

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
        """
        Delete the specified Customer from contacthub
        :param customer: a Customer object representing the customer to delete
        :return: an object representing the deleted customer
        """
        return self.customer_api_manager.delete(customer=customer)

    def add_customer(self, customer, force_update=False):
        """
        Add a new customer in contacthub. If the customer already exist and force update is true, this method will update
        the entire customer with new data
        :param customer: a Customer object representing the customer to add
        :param force_update: a flag for update an already present customer
        :return: the customer added or updated
        """
        return self.customer_api_manager.post(customer=customer, force_update=force_update)

    def update_customer(self, customer, full_update=False):
        """
        Update a customer in contacthub with new data. If full_update is true, this method will update the full customer (PUT)
        and not only the changed data (PATCH)
        :param customer: a Customer object representing the customer to update
        :param full_update: a flag for execute a full update to the customer
        :return: the customer updated
        """
        if full_update:
            return self.customer_api_manager.put(customer=customer)
        else:
            return self.customer_api_manager.patch(customer=customer)

    def add_customer_session(self, customer, session_id):
        """
        Add a new session id for a customer.
        :param customer: the customer object for adding the session id
        :param session_id: a session id for create a new session
        :return: the session id of the new session inserted
        """
        return self.session_api_manager.post(customer=customer, session_id=session_id)

    @staticmethod
    def create_session_id():
        """
        Create a new random session id conformed to the UUID standard
        :return: a new session id conformed to the UUID standard
        """
        return uuid.uuid4()

    def add_tag(self, customer, tag):
        """
        Add a new tag in the list of customer's tags
        :param customer: the Customer object for adding the tag
        :param tag: a string, int, representing the tag to add
        """
        customer = self.get_customer(id=customer.id)
        new_tags = customer.tags.manual
        new_tags += [tag]
        customer.tags.manual = new_tags
        self.update_customer(customer)

    def remove_tag(self, customer, tag):
        """
        Remove (if exists) a tag in the list of customer's tag
        :param customer: the Customer object for adding the tag
        :param tag: a string, int, representing the tag to add
        """
        customer = self.get_customer(id=customer.id)
        new_tags = list(customer.tags.manual)
        try:
            new_tags.remove(tag)
            customer.tags.manual = new_tags
            self.update_customer(customer)
        except ValueError as e:
            raise ValueError("Tag not in Customer's Tags")






