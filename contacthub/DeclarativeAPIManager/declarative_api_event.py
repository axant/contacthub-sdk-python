# -*- coding: utf-8 -*-
from contacthub.APIManager.api_event import EventAPIManager
from contacthub.DeclarativeAPIManager.declarative_api_base import BaseDeclarativeApiManager
from contacthub.models.event import Event


class EventDeclarativeApiManager(BaseDeclarativeApiManager):
    """
    Declarative class for retrieving Events data, that offers an interface between the Nodes and the APIManager level.
    This class interact with high level Event model.
    """

    def __init__(self, node):
        super(EventDeclarativeApiManager, self).__init__(node=node, api_manager=EventAPIManager, entity=Event)

    def get_all(self, customer_id, read_only=False):
        """
        Get all events
        :param read_only:
        :param customer_id: the id of the customer owner of the event
        :return: a list of Event object
        """
        return super(EventDeclarativeApiManager, self).get_all(customer_id=customer_id, read_only=read_only)