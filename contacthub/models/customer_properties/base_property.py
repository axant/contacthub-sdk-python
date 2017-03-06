
class BaseProperty(object):
    def __init__(self, properties):
        self.properties = properties

    def __getattr__(self, item):
        return self.properties[item]