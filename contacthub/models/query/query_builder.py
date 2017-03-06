from copy import deepcopy

from contacthub.models.query.query import Query
from contacthub.models.query.criterion import Criterion


class QueryBuilder(object):
    def __init__(self, node, entity):
        self.entity = entity
        self.node = node

    def filter(self, criterion):
        query_ret = {'query':
                 {'type': '', 'name': 'query', 'are': {'condition': ''}
                  }
             }
        query_ret['query']['type'] = 'simple'
        query_ret['query']['are']['condition'] = self._filter(criterion)
        return Query(node=self.node, query=query_ret)

    def _filter(self, criterion):
        if criterion.operator in Criterion.SIMPLE_OPERATORS.OPERATORS:
            atomic_query = {'type': 'atomic', 'attribute': '', 'operator': ''}
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

            atomic_query['attribute'] = attribute
            atomic_query['operator'] = criterion.operator
            if criterion.second_element:
                atomic_query['value'] = criterion.second_element
            return atomic_query
        else:
            if criterion.operator in Criterion.COMPLEX_OPERATORS.OPERATORS:
                composite_query = {'type': 'composite', 'conjunction': '', 'conditions': []}
                composite_query['conjunction'] = criterion.operator
                first_element = self._filter(criterion.first_element)
                second_element = self._filter(criterion.second_element)
                composite_query['conditions'].append(first_element)
                composite_query['conditions'].append(second_element)

                return composite_query
