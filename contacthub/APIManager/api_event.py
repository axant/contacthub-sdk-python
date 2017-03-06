from contacthub.APIManager.api_base import BaseAPIManager


class EventAPIManager(BaseAPIManager):
    """
    A wrapper for the orginal API regarding the events data. This is the lowest level for retrieving data from the API.
    Implements the BaseAPIManager class
    """

    def __init__(self, node):
        """

        :param node: the Node object for retrieving Events data
        """
        super(EventAPIManager, self).__init__(node, 'events')











