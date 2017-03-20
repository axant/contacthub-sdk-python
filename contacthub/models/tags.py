

class Tags(object):
    """
    Tags property of the Customer model
    """
    __slots__ = ('json_properties',)

    def __init__(self, json_properties):
        self.json_properties=json_properties

    def __getattr__(self, item):
        """
       Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
       element is datetime format, return a datetime object
       :param item: the key of the base property dict
       :return: an element of the dictionary, or datetime object if element associated at the key contains a datetime format object
       """
        try:
            return self.json_properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" % (type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Tags, self).__setattr__(attr, val)
        else:
            self.json_properties[attr] = val