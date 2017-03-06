class Criterion(object):

    class COMPLEX_OPERATORS:
        AND = 'and'
        OR = 'or'
        OPERATORS = [AND, OR]

    class SIMPLE_OPERATORS:
        EQUALS = 'EQUALS'
        NOT_EQUALS = 'NOT_EQUALS'
        GT = 'GT'
        GTE = 'GTE'
        LT = 'LT'
        LTE = 'LTE'
        IN = 'IN'
        NOT_IN = 'NOT_IN'
        IS_NULL = 'IS_NULL'
        IS_NOT_NULL = 'IS_NOT_NULL'

        BETWEEN = 'BEETWEEN'

        OPERATORS = [EQUALS, NOT_EQUALS, GT, GTE, LT, LTE, IN, NOT_IN, IS_NULL, IS_NOT_NULL, BETWEEN]

    def __init__(self, first_element, operator, second_element=None):
        self.first_element = first_element
        self.operator = operator
        self.second_element = second_element

    def __and__(self, criterion):
        return Criterion(self, Criterion.COMPLEX_OPERATORS.AND, criterion)

    def __or__(self, criterion):
        return Criterion(self, Criterion.COMPLEX_OPERATORS.OR, criterion)


