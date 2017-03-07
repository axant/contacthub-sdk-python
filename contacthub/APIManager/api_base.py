# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class BaseAPIManager(object):
    """
    Base class for APIManager classes, every APIManager should implements the following methods.
    This is the lowest level for retrieving data from the API.
    """

    __metaclass__ = ABCMeta

    def __init__(self, node, entity):
        """

        :param node: the Node object for retrieve the entity data
        :param entity: a String representing the entity on which the API will operate
        """
        self.node = node
        self.request_url = self.node.workspace.base_url + '/' + self.node.workspace.workspace_id + '/' + entity
        self.headers = {'Authorization': 'Bearer ' + self.node.workspace.token}

    @abstractmethod
    def get_all(self):
        """
        GET method for retrieving all resources of an entity
        """

    # @abstractmethod
    # def get(self, res_id):
    #     """
    #
    #     """
    #     pass
    #
    # @abstractmethod
    # def delete(self, res_id):
    #     """
    #
    #     """
    #     pass
    #
    # @abstractmethod
    # def put(self, res_id):
    #     """
    #
    #     """
    #     pass
    #
    # def post(self, res_id):
    #     """
    #
    #     """
    #     pass
    #
    # @abstractmethod
    # def patch(self, res_id):
    #     """
    #
    #     """
    #     pass
