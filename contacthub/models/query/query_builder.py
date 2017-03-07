from copy import deepcopy

from contacthub.models.customer import Customer
from contacthub.models.query.query import Query
from contacthub.models.query.criterion import Criterion


class QueryBuilder(object):
    """
    Query builder class for converting a Criteria Object to API-like query for ContactHub APIs.
    """
    def __init__(self, node, entity):
        """
        :param node: The node where to find entities for the query
        :param entity: The entity on wich to apply a query.
        """
        self.entity = entity
        self.node = node

    def filter(self, criterion):
        """
        Create a new API Like query for ContactHub APIs (JSON Format)
        :param criterion: the Criterion object for fields for query data
        :return: a Query object containing the JSON object representing a query for the APIs
        """
        query_ret = {'query':
                 {'type': 'simple', 'name': 'query', 'are': {}
                  }
             }
        query_ret['query']['are']['condition'] = self._filter(criterion)
        return Query(node=self.node, query=query_ret, entity=self.entity)

    def _filter(self, criterion):
        """
        Private function for creating atomic or composite subqueries found in major query.
        :param criterion: the Criterion object for fields for query data
        :return: a JSON object containing a subquery for creating the query for the APIs
        """
        if criterion.operator in Criterion.SIMPLE_OPERATORS.OPERATORS:
            atomic_query = {'type': 'atomic'}
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
                composite_query = {'type': 'composite', 'conditions': []}
                composite_query['conjunction'] = criterion.operator
                first_element = self._filter(criterion.first_element)
                second_element = self._filter(criterion.second_element)
                composite_query['conditions'].append(first_element)
                composite_query['conditions'].append(second_element)

                return composite_query
