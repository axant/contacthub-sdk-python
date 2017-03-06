from contacthub.models.customer_properties.base_property import BaseProperty


class Geo(BaseProperty):
    pass


class Address(BaseProperty):
    SUBPROPERTIES = {'geo': Geo}

    def __getattr__(self, item):
        if self.properties[item] is None:
            return None

        if item in self.SUBPROPERTIES:
            return self.SUBPROPERTIES[item](self.properties[item])
        return self.properties[item]
