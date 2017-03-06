from contacthub.models.query.criterion import Criterion


class EntityField(object):

    def __init__(self, entity, field):
        self.entity = entity
        self.field = field

    def __getattr__(self, item):
        return EntityField(self, item)

    def __eq__(self, other):
        return Criterion(self, Criterion.SIMPLE_OPERATORS.EQUALS, other)

    def __ne__(self, other):
        return Criterion(self, Criterion.SIMPLE_OPERATORS.NOT_EQUALS, other)

    def __lt__(self, other):
        return Criterion(self, Criterion.SIMPLE_OPERATORS.LT, other)

    def __le__(self, other):
        return Criterion(self, Criterion.SIMPLE_OPERATORS.LTE, other)

    def __gt__(self, other):
        return Criterion(self, Criterion.SIMPLE_OPERATORS.GT, other)

    def __ge__(self, other):
        return Criterion(self, Criterion.SIMPLE_OPERATORS.GTE, other)

    def _in(self, _list):
        if type(_list) is not list:
            raise Exception("The comparision value should be a list.")

        return Criterion(self, Criterion.SIMPLE_OPERATORS.IN, _list)

    def _not_in(self, _list):
        if type(_list) is not list:
            raise Exception("The comparision value should be a list.")
        return Criterion(self, Criterion.SIMPLE_OPERATORS.NOT_IN, _list)

    def _is_null(self):
        return Criterion(self, Criterion.SIMPLE_OPERATORS.IS_NULL)

    def _is_not_null(self):
        return Criterion(self, Criterion.SIMPLE_OPERATORS.IS_NOT_NULL)