# -*- coding: utf-8 -*-
from contacthub.APIManager.api_customer import CustomerAPIManager
from contacthub.DeclarativeAPIManager.declarative_api_base import BaseDeclarativeApiManager

class CustomerDeclarativeApiManager(BaseDeclarativeApiManager):
    """
    Declarative class for retrieving Customers data, that offers an interface between the Nodes and the APIManager level.
    This class interact with high level Customer model.
    """

    def __init__(self, node, entity):
        super(CustomerDeclarativeApiManager, self).__init__(node=node, api_manager=CustomerAPIManager, entity=entity)

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

    def post(self, customer, force_update=False):
        """
        Insert a new customer
        :param force_update: Force an update if the customer is already present in CH.
        If the POST method return status code 409 and the force update flag is true, this method execute a patch in
        for the customer already in CH.
        :param customer: a customer object to insert in customers
        :return:
        """
        return super(CustomerDeclarativeApiManager, self).post(body=customer.json_properties, force_update=force_update)

    def delete(self, customer):
        """
        Delete the customer associated at the specified id
        :param _id: the id of the customer to delete
        :return: the deleted Customer object
        """
        return super(CustomerDeclarativeApiManager, self).delete(_id=customer.id)



