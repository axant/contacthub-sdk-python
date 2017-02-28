

class Customer(object):
    __slots__ = ('customer',)
    SUBPROPERTIES = ('base', 'extended', 'extra')

    def __init__(self, customer):
        self.customer = customer

    def __getattr__(self, item):
        if item in self.SUBPROPERTIES:
            if self.customer[item] is None:
                self.customer[item] = dict()
            return Customer(self.customer[item])
        else:
            return self.customer[item]

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Customer, self).__setattr__(attr, val)
        else:
            self.customer[attr] = val


