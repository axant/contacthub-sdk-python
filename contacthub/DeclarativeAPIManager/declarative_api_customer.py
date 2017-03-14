# -*- coding: utf-8 -*-
from contacthub.APIManager.api_customer import CustomerAPIManager
from contacthub.DeclarativeAPIManager.declarative_api_base import BaseDeclarativeApiManager
from contacthub.models.customer import Customer


class CustomerDeclarativeApiManager(BaseDeclarativeApiManager):
    """
    Declarative class for retrieving Customers data, that offers an interface between the Nodes and the APIManager level.
    This class interact with high level Customer model.
    """

    def __init__(self, node):
        super(CustomerDeclarativeApiManager, self).__init__(node=node, api_manager=CustomerAPIManager, entity=Customer)

    def get_all(self, query=None, externalId=None, page=None, size=None):
        """
        Retrieve all customers from the APIManager
        :param query: A JSON format query for filter the custumers data
        :return: A list containing Customer object fetched from API
        """
        return super(CustomerDeclarativeApiManager, self).get_all(query=query, externalId=externalId, page=page, size=size)

    def get(self, id=None, externalId=None):
        """
        GET a single Customer object by its ID or externalID
        :param id:
        :param externalId:
        :return: a Customer object for the given ID or exernalID
        """
        return super(CustomerDeclarativeApiManager, self).get(id=id, externalId=externalId)

    def post(self, customer):
        """
        Insert a new customer
        :param customer: a customer object to insert in customers
        :return:
        """
        return super(CustomerDeclarativeApiManager, self).post(body=customer.json_properties)

