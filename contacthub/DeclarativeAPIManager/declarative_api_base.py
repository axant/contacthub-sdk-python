# -*- coding: utf-8 -*-
from contacthub.lib.read_only_list import ReadOnlyList


class BaseDeclarativeApiManager(object):
    """
    Base class for DeclarativeAPIManager classes, every DeclarativeAPIManager should implements the following methods.
    """

    def __init__(self, node, api_manager, entity):
        self.node = node
        self.api_manager = api_manager
        self.entity = entity

    def get_all(self, *args, **kwargs):
        """
        Get all elements associated to an entity.
        :param read_only:
        :param args:
        :param kwargs:
        :return: A list containing specified entity object fetched from API
        """
        entities = []
        resp = self.api_manager(node=self.node).get_all(**kwargs)
        for entity in resp['elements']:
            entities.append(self.entity(entity, node=self.node))
        return entities if not kwargs.get('read_only', False) else ReadOnlyList(entities)

    def get(self, *args, **kwargs):
        """
        Get all elements associated to an entity.
        :param read_only:
        :param args:
        :param kwargs:
        :return: A list containing specified entity object fetched from API
        """
        id = kwargs.get('id', None)
        externalId = kwargs.get('externalId', None)
        if id and externalId:
            raise ValueError('Cannot get a customer by both its id and externalId')
        if not id and not externalId:
            raise ValueError('Insert an id or an externalId')

        if externalId:
            customers = self.get_all(externalId=externalId)
            if len(customers) == 1:
                return customers[0]

        else:
            return self.entity(self.api_manager(node=self.node).get(_id=id))


    def post(self, *args, **kwargs):
        """
        Post a new element in an entity.
        :param args:
        :param kwargs:
        :return: a
        """
        return self.entity(self.api_manager(node=self.node).post(**kwargs))

