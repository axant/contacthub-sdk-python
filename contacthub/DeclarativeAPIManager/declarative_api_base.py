# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class BaseDeclarativeApiManager(object):
    __metaclass__ = ABCMeta

    def __init__(self, node):
        self.node = node

    @abstractmethod
    def get_all(self):
        pass
