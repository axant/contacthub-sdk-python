from contacthub.models.customer_properties.property import Property


class Geo(Property):
    """
    Geo sub property of the Andress property
    """
    pass


class Address(Property):
    """
    Login Credential sub property of CustomerBaseProperties
    """

    SUBPROPERTIES = {'geo': Geo}

    def __getattr__(self, item):
        if item in self.SUBPROPERTIES:
            return self.SUBPROPERTIES[item](self.properties[item])
        try:
            return self.properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))
