# -*- coding: utf-8 -*-
from contacthub.APIManager.api_customer import CustomerAPIManager


class SessionDeclarativeAPIManager(object):
    """
    Declarative class for retrieving Customers data, that offers an interface between the Nodes and the APIManager level.
    This class interact with high level Customer model.
    """

    def __init__(self, node):
        self.node = node
        self.customer_api_manager = CustomerAPIManager(node=self.node)

    def post(self, customer, session_id):
        """
        Insert a new customer
        :param force_update: Force an update if the customer is already present in CH.
        If the POST method return status code 409 and the force update flag is true, this method execute a patch in
        for the customer already in CH.
        :param customer: a customer object to insert in customers
        :return:
        """
        body = {'value': str(session_id)}
        return self.customer_api_manager.post(body=body, urls_extra='/' + customer.id + '/sessions')['value']






