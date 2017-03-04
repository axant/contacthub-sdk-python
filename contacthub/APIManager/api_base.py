class BaseAPIManager(object):
    """
    Base class for APIManager, every APIManager should implements following methods:
        - get_all
        - get
        - delete
        - put
        - post
        - patch
    """

    def __init__(self, node, entity):
        self.node = node
        self.request_url = self.node.workspace.base_url + '/' + self.node.workspace.workspace_id + '/' + entity
        self.headers = {'Authorization': 'Bearer ' + self.node.workspace.token}

    def get_all(self):
        """

        """
        pass

    def get(self):
        """

        """
        pass

    def delete(self):
        """

        """
        pass

    def put(self):
        """

        """
        pass

    def post(self):
        """

        """
        pass

    def patch(self):
        """

        """
        pass










