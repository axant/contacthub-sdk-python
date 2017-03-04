# -*- coding: utf-8 -*-
from contacthub.APIManager.api_customer import CustomerAPIManager
from contacthub.DeclarativeAPIManager.declarative_api_base import BaseDeclarativeApiManager
from contacthub.models.customer import Customer


class CustomerDeclarativeApiManager(BaseDeclarativeApiManager):

    def get_all(self, query=None):
        customers = []
        resp = CustomerAPIManager(node=self.node).get_all(query=query)
        for customer in resp['elements']:
            customers.append(Customer(customer))
        return customers
