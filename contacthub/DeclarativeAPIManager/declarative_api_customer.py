# -*- coding: utf-8 -*-
from contacthub.APIManager.api_customer import CustomerAPIManager
from contacthub.DeclarativeAPIManager.declarative_api_base import BaseDeclarativeApiManager
from contacthub.models.customer import Customer


class CustomerDeclarativeApiManager(BaseDeclarativeApiManager):
    """
    Declarative class for retrieving Customers data, that offers an interface between the Nodes and the APIManager level.
    This class interact with high level Customer model.
    """
    def get_all(self, query=None):
        """
        Retrieve all customers
        :param query:
        :return: A list containing Customer object
        """
        customers = []
        resp = CustomerAPIManager(node=self.node).get_all(query=query)
        for customer in resp['elements']:
            customers.append(Customer(customer))
        return customers
