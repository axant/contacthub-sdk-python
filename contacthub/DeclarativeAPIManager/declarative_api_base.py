# -*- coding: utf-8 -*-


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
        :param args:
        :param kwargs:
        :return: A list containing specified entity object fetched from API
        """
        entities = []
        resp = self.api_manager(node=self.node).get_all(**kwargs)
        for entity in resp['elements']:
            entities.append(self.entity(entity, node=self.node))
        return entities

    def post(self, *args, **kwargs):
        """
        Post a new element in an entity.
        :param args:
        :param kwargs:
        :return: a
        """
        return self.entity(self.api_manager(node=self.node).post(**kwargs))

