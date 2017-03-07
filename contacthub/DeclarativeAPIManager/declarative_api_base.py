# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class BaseDeclarativeApiManager(object):
    """
    Base class for DeclarativeAPIManager classes, every DeclarativeAPIManager should implements the following methods.
    """
    __metaclass__ = ABCMeta

    def __init__(self, node):
        self.node = node

    @abstractmethod
    def get_all(self):
        """
        Get all elements associated to an entity.
        """