from datetime import datetime



class Job(object):
    """
    Job model
    """
    DATE_PROPERTIES = {'startDate': "%Y-%m-%d", 'endDate': "%Y-%m-%d"}

    def __init__(self, **properties):
        self.properties=properties

    def __getattr__(self, item):
        """
       Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
       element is datetime format, return a datetime object
       :param item: the key of the base property dict
       :return: an element of the dictionary, or datetime object if element associated at the key contains a datetime format object
       """
        if item in self.DATE_PROPERTIES:
            return datetime.strptime(self.properties[item], self.DATE_PROPERTIES[item])
        try:
            return self.properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))
