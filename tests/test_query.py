import json
import unittest

import mock
from datetime import datetime

from contacthub.models.customer import Customer
from contacthub.models.query import between_
from contacthub.models.query.criterion import Criterion
from contacthub.models.query.entity_field import EntityField
from contacthub.models.query.entity_meta import EntityMeta
from contacthub.models.query.query import Query
from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestQuery(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.entity_field = (Customer.attr)
        w = Workspace(workspace_id=123, token=456)
        cls.node = w.get_node(123)
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'

    @classmethod
    def tearDown(cls):
        pass

    def test_enitity_field_get_attr(self):
        e1 = EntityField(Customer, 'attr1')
        e2 = EntityField(e1, 'attr2')
        e = Customer.attr1.attr2
        assert isinstance(e, EntityField), type(e)
        assert isinstance(e.entity, EntityField), type(e.entity)
        assert e.entity == e2.entity, e.entity
        assert e.field == e2.field, e.field
        assert e.entity.field == e2.entity.field, e.entity

    def test_entity_field_eq(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.EQUALS, 'attr')
        c = (Customer.attr == 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_neq(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.NOT_EQUALS, 'attr')
        c = (Customer.attr != 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_lt(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.LT, 'attr')
        c = (Customer.attr < 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_le(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.LTE, 'attr')
        c = (Customer.attr <= 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_gt(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.GT, 'attr')
        c = (Customer.attr > 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_ge(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.GTE, 'attr')
        c = (Customer.attr >= 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_null(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.IS_NULL)
        c = (Customer.attr == None)
        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element is None, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_not_null(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.IS_NOT_NULL)
        c = (Customer.attr != None)

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element is None, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_meta(self):
        assert isinstance(Customer.attr1, EntityField), type(Customer.attr1)

    def test_criterion_and(self):
        c1 = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.IS_NOT_NULL)
        c2 = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.EQUALS, 'attr')

        c3 = c1 & c2

        assert isinstance(c3, Criterion), type(c3)
        assert isinstance(c3.first_element, Criterion), type(c3.first_element)
        assert c3.first_element.operator == c1.operator, c3.first_element.operator
        assert isinstance(c3.second_element, Criterion), type(c3.second_element)
        assert c3.second_element.operator == c2.operator, c3.first_element.operator
        assert c3.operator == Criterion.COMPLEX_OPERATORS.AND

    def test_criterion_or(self):
        c1 = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.IS_NOT_NULL)
        c2 = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.EQUALS, 'attr')
        c3 = c1 | c2
        assert isinstance(c3, Criterion), type(c3)
        assert isinstance(c3.first_element, Criterion), type(c3.first_element)
        assert c3.first_element.operator == c1.operator, c3.first_element.operator
        assert isinstance(c3.second_element, Criterion), type(c3.second_element)
        assert c3.second_element.operator == c2.operator, c3.first_element.operator
        assert c3.operator == Criterion.COMPLEX_OPERATORS.OR

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_between(self, mock_get):
        self.node.query(Customer).filter(between_(Customer.base.dob, datetime(2011,12,11), datetime(2015,12,11))).all()
        params = {'nodeId':self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
                              {'type': 'simple', 'name': 'query', 'are':
                                  {'condition':
                                       { 'type': 'atomic', 'attribute': 'base.dob', 'operator': 'BETWEEN', 'value': ['2011-12-11T00:00:00', '2015-12-11T00:00:00']}}},
                                      })
        mock_get.assert_called_with(self.base_url,headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_between_str(self, mock_get):
        self.node.query(Customer).filter(
            between_(Customer.base.dob, '2011-12-11', '2015-12-11')).all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query','query':
                                          {'type': 'simple', 'name': 'query', 'are':
                                              {'condition':
                                                   {'type': 'atomic','attribute': 'base.dob','operator': 'BETWEEN',
                                                    'value': ['2011-12-11', '2015-12-11']}}}
                                      })

        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)


