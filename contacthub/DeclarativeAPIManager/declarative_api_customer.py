# -*- coding: utf-8 -*-
from contacthub.APIManager.api_customer import CustomerAPIManager
from contacthub.customer import Customer


class CustomerDeclarativeApiManager(object):

    def __init__(self, node):
        self.node = node

    @property
    def get_all(self):
        customers = []
        resp = CustomerAPIManager(node=self.node).get_all()
        for customer in resp['elements']:
            customers.append(Customer(customer))
        return customers
