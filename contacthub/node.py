# -*- coding: utf-8 -*-
from contacthub.api_manager.api_customer import CustomerAPIManager
from contacthub.lib.utils import resolve_mutation_tracker

from contacthub.models.customer import Customer
from contacthub.models.education import Education
from contacthub.models.job import Job
from contacthub.models.like import Like
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
        self.customer_api_manager = CustomerAPIManager(node=self)

    def get_customers(self, externalId=None, page=None, size=None):
        """
        Get all the customers in this node
        :return: A list containing Customer object of a node
        """
        customers = []
        resp = self.customer_api_manager.get_all(externalId=externalId, page=page, size=size)
        for customer in resp['elements']:
            customers.append(Customer(node=self, **customer))
        return customers

    def get_customer(self, id=None, externalId=None):
        if id and externalId:
            raise ValueError('Cannot get a customer by both its id and externalId')
        if not id and not externalId:
            raise ValueError('Insert an id or an externalId')

        if externalId:
            customers = self.get_customers(externalId=externalId)
            if len(customers) == 1:
                return customers[0]
            else:
                return customers
        else:
            return Customer(node=self, **self.customer_api_manager.get(_id=id))

    def query(self, entity):
        """
        Create a QueryBuilder object for a given entity, that allows to filter the entity's data
        :param entity: A class of model on which to run the query
        :return: A QueryBuilder object for the specified entity
        """
        return Query(node=self, entity=entity)

    def delete_customer(self, id, **attributes):
        """
        Delete the specified Customer from contacthub
        :param customer: a Customer object representing the customer to delete
        :return: an object representing the deleted customer
        """
        return Customer(node=self, **self.customer_api_manager.delete(_id=id))

    def add_customer(self, force_update=False, **attributes):
        """
        Add a new customer in contacthub. If the customer already exist and force update is true, this method will update
        the entire customer with new data
        :param customer: a Customer object representing the customer to add
        :param force_update: a flag for update an already present customer
        :return: the customer added or updated
        """
        return Customer(node=self, **self.customer_api_manager.post(body=attributes, force_update=force_update))

    def update_customer(self, id, full_update=False, **attributes):
        """
        Update a customer in contacthub with new data. If full_update is true, this method will update the full customer (PUT)
        and not only the changed data (PATCH)
        :param customer: a Customer object representing the customer to update
        :param full_update: a flag for execute a full update to the customer
        :return: the customer updated
        """

        if full_update:
            attributes['id'] = id
            return Customer(node=self, **self.customer_api_manager.put(_id=id, body=attributes))
        else:
            return Customer(node=self, **self.customer_api_manager.patch(_id=id, body=attributes))

    def add_customer_session(self, session_id, id, **attributes):
        """
        Add a new session id for a customer.
        :param customer_id: the customer ID for adding the session id
        :param session_id: a session ID for create a new session
        :return: the session id of the new session inserted
        """
        body = {'value': str(session_id)}
        return self.customer_api_manager.post(body=body, urls_extra=id + '/sessions')['value']

    @staticmethod
    def create_session_id():
        """
        Create a new random session id conformed to the UUID standard
        :return: a new session id conformed to the UUID standard
        """
        return uuid.uuid4()

    def add_tag(self, customer_id, tag):
        """
        Add a new tag in the list of customer's tags
        :param customer: the Customer object for adding the tag
        :param tag: a string, int, representing the tag to add
        """
        customer = self.get_customer(id=customer_id)
        new_tags = customer.tags.manual
        new_tags += [tag]
        customer.tags.manual = new_tags
        print(customer.mute)
        self.update_customer(id=customer_id, **resolve_mutation_tracker(customer.mute))

    def remove_tag(self, customer_id, tag):
        """
        Remove (if exists) a tag in the list of customer's tag
        :param customer_id: the Customer object for adding the tag
        :param tag: a string, int, representing the tag to add
        """
        customer = self.get_customer(id=customer_id)
        new_tags = list(customer.tags.manual)
        try:
            new_tags.remove(tag)
            customer.tags.manual = new_tags
            self.update_customer(id=customer_id, **resolve_mutation_tracker(customer.mute))
        except ValueError as e:
            raise ValueError("Tag not in Customer's Tags")

    def add_job(self, customer_id, **attributes):
        """
        Insert a new Job for the given Customer
        :param job: the new Job object to insert in the customer's job
        :param customer: a customer object for inserting the job
        :return: a Job object representing the added Job
        """
        entity_attrs = self.customer_api_manager.post(body=attributes, urls_extra=customer_id + '/jobs')
        return Job(customer=self.get_customer(id=customer_id), **entity_attrs)

    def remove_job(self, customer_id, id, **attributes):
        """
        Remove a the given Job for the given Customer
        :param job: the Job object to remove from the customer's job
        :param customer: a customer object for removing the job
        """
        self.customer_api_manager.delete(_id=customer_id, urls_extra='jobs/' + id)

    def update_job(self, customer_id, id, **attributes):
        """
        Update the given job of the given customer with new data
        ::param job: the Job object to update in the customer's job
        :param customer: a customer object for updating the job
        :return: a Job object representing the updated Job
        """
        entity_attrs = self.customer_api_manager.put(_id=customer_id, body=attributes, urls_extra='jobs/' + id)
        return Job(customer=self.get_customer(id=customer_id), **entity_attrs)

    def add_like(self, customer_id, **attributes):
        """
        Insert a new Job for the given Customer
        :param job: the new Job object to insert in the customer's job
        :param customer: a customer object for inserting the job
        :return: a Job object representing the added Job
        """
        entity_attrs = self.customer_api_manager.post(body=attributes, urls_extra=customer_id + '/likes')
        return Like(customer=self.get_customer(id=customer_id), **entity_attrs)

    def remove_like(self, customer_id, id, **attributes):
        """
        Remove a the given Job for the given Customer
        :param job: the Job object to remove from the customer's job
        :param customer: a customer object for removing the job
        """
        self.customer_api_manager.delete(_id=customer_id, urls_extra='likes/' + id)

    def update_like(self, customer_id, id, **attributes):
        """
        Update the given job of the given customer with new data
        ::param job: the Job object to update in the customer's job
        :param customer: a customer object for updating the job
        :return: a Job object representing the updated Job
        """
        entity_attrs = self.customer_api_manager.put(_id=customer_id, body=attributes, urls_extra='likes/' + id)
        return Like(customer=self.get_customer(id=customer_id), **entity_attrs)

    def add_education(self, customer_id, **attributes):
        """
        Insert a new Job for the given Customer
        :param job: the new Job object to insert in the customer's job
        :param customer: a customer object for inserting the job
        :return: a Job object representing the added Job
        """
        entity_attrs = self.customer_api_manager.post(body=attributes, urls_extra=customer_id + '/educations')
        return Education(customer=self.get_customer(id=customer_id), **entity_attrs)

    def remove_education(self, customer_id, id, **attributes):
        """
        Remove a the given Job for the given Customer
        :param job: the Job object to remove from the customer's job
        :param customer: a customer object for removing the job
        """
        self.customer_api_manager.delete(_id=customer_id, urls_extra='educations/' + id)

    def update_education(self, customer_id, id, **attributes):
        """
        Update the given job of the given customer with new data
        ::param job: the Job object to update in the customer's job
        :param customer: a customer object for updating the job
        :return: a Job object representing the updated Job
        """
        entity_attrs = self.customer_api_manager.put(_id=customer_id, body=attributes, urls_extra='educations/' + id)
        return Education(customer=self.get_customer(id=customer_id), **entity_attrs)








