class ReadOnlyList(list):

    def NotImplemented(self, *args, **kw):
        raise ValueError("Read Only list proxy")

    remove  = reverse = append = pop = extend = insert = __setitem__ = __setslice__ = __delitem__ = NotImplemented