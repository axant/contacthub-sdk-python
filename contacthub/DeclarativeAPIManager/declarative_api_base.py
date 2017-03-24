# -*- coding: utf-8 -*-
from contacthub.lib.read_only_list import ReadOnlyList


class BaseDeclarativeApiManager(object):
    """
    Base class for DeclarativeAPIManager classes, every DeclarativeAPIManager should implements the following methods.
    """

    def __init__(self, node, api_manager, entity):
        self.node = node
        self.api_manager = api_manager(node=self.node)
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
        resp = self.api_manager.get_all(**kwargs)
        for entity in resp['elements']:
            entities.append(self.entity.from_dict(node=self.node, internal_properties=entity))
        return entities if not kwargs.get('read_only', False) else ReadOnlyList(entities)

    def get(self, *args, **kwargs):
        """
        Get all elements associated to an entity.
        :param read_only:
        :param args:
        :param kwargs:
        :return: A list containing specified entity object fetched from API
        """
        return self.entity(node=self.node, **self.api_manager.get(**kwargs))

    def post(self, *args, **kwargs):
        """
        Post a new element in an entity.
        :param args:
        :param kwargs:
        :return: a
        """
        return self.entity(node=self.node, **self.api_manager.post(**kwargs))

    def delete(self, *args, **kwargs):
        """
        Delete an element in an entity
        :param id: the id of the entity's element to delete
        """
        return self.entity.from_dict(node=self.node, internal_properties=self.api_manager.delete(**kwargs))

    def patch(self, *args, **kwargs):
        """
        Delete an element in an entity
        :param id: the id of the entity's element to delete
        """
        return self.entity.from_dict(node=self.node, internal_properties=self.api_manager.patch(**kwargs))

    def put(self, *args, **kwargs):
        """
        Delete an element in an entity
        :param id: the id of the entity's element to delete
        """
        return self.entity.from_dict(node=self.node, internal_properties=self.api_manager.put(**kwargs))


