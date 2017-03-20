# -*- coding: utf-8 -*-
from contacthub.APIManager.api_customer import CustomerAPIManager
from contacthub.DeclarativeAPIManager.declarative_api_base import BaseDeclarativeApiManager
from copy import deepcopy


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
        if id and externalId:
            raise ValueError('Cannot get a customer by both its id and externalId')
        if not id and not externalId:
            raise ValueError('Insert an id or an externalId')

        if externalId:
            customers = self.get_all(externalId=externalId)
            if len(customers) == 1:
                return customers[0]
            else:
                return customers
        else:
            return super(CustomerDeclarativeApiManager, self).get(_id=id)

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
        Delete the given customer
        :param customer: the customer to delete
        :return: the deleted Customer object
        """
        return super(CustomerDeclarativeApiManager, self).delete(_id=customer.id)

    def patch(self, customer):
        """
        Patch the given customer
        :param full_update:
        :param customer: the id of the customer to delete
        :return: the patched Customer object
        """

        body = {}
        for key in customer.mute:
            update_dictionary = body
            splitted = key.split('.')
            last_element = splitted[-1:][0]
            for attr in splitted:
                if attr == last_element:
                    update_dictionary[attr] = customer.mute[key]
                else:
                    if attr not in update_dictionary:
                        update_dictionary[attr] = {}
                    update_dictionary = update_dictionary[attr]
        body['extended'] = customer.json_properties['extended']

        return super(CustomerDeclarativeApiManager, self).patch(_id=customer.id, body=body)

    def put(self, customer):
        body = deepcopy(customer.json_properties)
        body.pop('registeredAt', None)
        body.pop('updatedAt', None)
        body.pop('id', None)
        if 'base' in body and 'timezone' in body['base'] and body['base']['timezone'] is None:
            body['base']['timezone'] = 'Europe/Rome'
        return super(CustomerDeclarativeApiManager, self).put(_id=customer.id, body=body)




