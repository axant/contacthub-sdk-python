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
            entities.append(self.entity(json_properties=entity, node=self.node))
        return entities if not kwargs.get('read_only', False) else ReadOnlyList(entities)

    def get(self, *args, **kwargs):
        """
        Get all elements associated to an entity.
        :param read_only:
        :param args:
        :param kwargs:
        :return: A list containing specified entity object fetched from API
        """
        return self.entity(self.api_manager(node=self.node).get(**kwargs))

    def post(self, *args, **kwargs):
        """
        Post a new element in an entity.
        :param args:
        :param kwargs:
        :return: a
        """
        return self.entity(node=self.node, json_properties=self.api_manager(node=self.node).post(**kwargs))

    def delete(self, *args, **kwargs):
        """
        Delete an element in an entity
        :param id: the id of the entity's element to delete
        """
        return self.entity(self.api_manager(node=self.node).delete(**kwargs))

    def patch(self, *args, **kwargs):
        """
        Delete an element in an entity
        :param id: the id of the entity's element to delete
        """
        return self.entity(node=self.node, json_properties=self.api_manager(node=self.node).patch(**kwargs))

    def put(self, *args, **kwargs):
        """
        Delete an element in an entity
        :param id: the id of the entity's element to delete
        """
        return self.entity(node=self.node,json_properties=self.api_manager(node=self.node).put(**kwargs))


