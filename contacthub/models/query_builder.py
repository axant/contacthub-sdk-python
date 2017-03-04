import json

from contacthub.models.criterion import Criterion
from contacthub.models.query import Query


class QueryBuilder(object):
    def __init__(self, node, entity):
        self.entity = entity
        self.node = node

    def filter(self, criterion):
        if criterion.operator in Criterion.SIMPLE_OPERATORS.OPERATORS:
            query_str = '''{{"query": {{"type": "simple","name": "query","are": {{"condition": {{"type": "atomic","attribute": "{attribute}","operator": "{operator}","value": "{value}"}}}}}}}}'''

            entity_field = criterion.first_element
            fields = [entity_field.field]

            while not type(entity_field.entity) is type(self.entity):
                entity_field = entity_field.entity
                fields.append(entity_field.field)

            attribute = ''
            for field in reversed(fields):
                attribute += field
                attribute += '.'

            attribute = attribute[:-1]

            formatted = query_str.format(attribute=attribute, operator=criterion.operator, value=criterion.second_element)

            return Query(node=self.node, criterion=formatted)
