from contacthub.api_manager.api_customer import CustomerAPIManager


class Like(object):
    """
    Like model
    """

    def __init__(self, customer=None, **attributes):
        self.customer = customer
        self.attributes = attributes
        self.customer_api_manager = CustomerAPIManager(node=customer.node)
        self.entity_name = 'likes'

    def __getattr__(self, item):
        """
       Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
       element is datetime format, return a datetime object
       :param item: the key of the base property dict
       :return: an element of the dictionary, or datetime object if element associated at the key contains a datetime format object
       """
        try:
            return self.attributes[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))

    def post(self):
        """
        Post this Education in the list of the Education for a Customer(specified in the constructor of the Education)
        :return: a Education object representing the posted Education
        """
        entity_attrs = self.customer_api_manager.post(body=self.attributes, urls_extra=self.customer.id + '/'
                                                                                   + self.entity_name)
        self.customer.base.educations += entity_attrs

    def delete(self):
        """
        Remove this Education from the list of the Education for a Customer(specified in the constructor of
        the Education)
        :return: a Education object representing the deleted Education
        """
        self.customer_api_manager.delete(_id=self.customer.id, urls_extra=self.entity_name + '/' + self.attributes['id'])

    def put(self):
        """
        Put this Education in the list of the Education for a Customer(specified in the constructor of the Education)
        :return: a Education object representing the putted Education
        """
        entity_attrs = self.customer_api_manager.put(_id=self.customer.id, body=self.attributes,
                                                 urls_extra=self.entity_name + '/' + self.attributes['id'])
        self.customer.base.educations += entity_attrs