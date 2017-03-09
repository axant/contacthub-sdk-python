
class Education(object):
    """
    Education model
    """

    def __init__(self, json_properties):
        self.json_properties=json_properties


    class SCHOOL_TYPES:
        """
        Subclasses with school types for the schoolType field of Education
        """
        PRIMARY_SCHOOL = 'PRIMARY_SCHOOL'
        SECONDARY_SCHOOL = 'SECONDARY_SCHOOL'
        HIGH_SCHOOL = 'HIGH_SCHOOL'
        COLLEGE = 'COLLEGE'
        OTHER = 'OTHER'

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
