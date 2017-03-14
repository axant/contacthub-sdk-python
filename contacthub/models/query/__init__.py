from contacthub.models.query.criterion import Criterion


def in_(value, list_entity):
    return Criterion(list_entity, Criterion.SIMPLE_OPERATORS.IN, value)


def not_in_(value, list_entity):
    return Criterion(list_entity, Criterion.SIMPLE_OPERATORS.NOT_IN, value)