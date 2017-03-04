class Criterion(object):

    class COMPLEX_OPERATORS:
        AND = 'AND'
        OR = 'OR'

    class SIMPLE_OPERATORS:
        EQUALS = 'EQUALS'
        OPERATORS = [EQUALS]

    def __init__(self, first_element, operator, second_element):
        self.first_element = first_element
        self.operator = operator
        self.second_element = second_element

    def __and__(self, query):
        return Criterion(self, Criterion.COMPLEX_OPERATORS.AND, query)

    def __or__(self, query):
        return Criterion(self, Criterion.COMPLEX_OPERATORS.OR, query)


