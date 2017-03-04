from contacthub.models.criterion import Criterion


class EntityField(object):

    def __init__(self, entity, field):
        self.entity = entity
        self.field = field

    def __eq__(self, other):
        return Criterion(self, Criterion.SIMPLE_OPERATORS.EQUALS, other)

    def __getattr__(self, item):
        return EntityField(self, item)