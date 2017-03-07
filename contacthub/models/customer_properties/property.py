
class Property(object):
    """
    Generic property for all entities
    """
    def __init__(self, properties):
        """
        :param properties: A dictionary with properties to return or set
        """
        self.properties = properties

    def __getattr__(self, item):
        try:
            return self.properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))