from contacthub.models.query.criterion import Criterion


class EntityField(object):
    """
    Class for creating Critierion object for queries.

    Use this class for handling all operation that you want to implements in queries syntax  and create new Criterion
    with related operations.
    """

    def __init__(self, entity, field):
        """
        :param entity: Entity
        :param field: field
        """
        self.entity = entity
        self.field = field

    def __getattr__(self, item):
        """
        Multiple level property handling, like Entity.field1.field2, creting a new EntityFiled object with
        Entity.field1 as entity and a field2 as field
        :param item: the field for creating an new EntityField object
        :return: a new EntityField object
        """
        return EntityField(self, item)

    def __eq__(self, other):
        """
        Overriding the == operator
        :param other: a value for fetching data
        :return: a new Criterion object representing the criteria for querying data
        """
        return Criterion(self, Criterion.SIMPLE_OPERATORS.EQUALS, other)

    def __ne__(self, other):
        """
        Overriding the != operator
        :param other: a value for fetching data
        :return:  a new Criterion object representing the criteria for querying data
        """
        return Criterion(self, Criterion.SIMPLE_OPERATORS.NOT_EQUALS, other)

    def __lt__(self, other):
        """
        Overriding the < operator
        :param other: a value for fetching data
        :return:  a new Criterion object representing the criteria for querying data
        """
        return Criterion(self, Criterion.SIMPLE_OPERATORS.LT, other)

    def __le__(self, other):
        """
        Overriding the >= operator
        :param other: a value for fetching data
        :return:  a new Criterion object representing the criteria for querying data
        """
        return Criterion(self, Criterion.SIMPLE_OPERATORS.LTE, other)

    def __gt__(self, other):
        """
        Overriding the > operator
        :param other: a value for fetching data
        :return:  a new Criterion object representing the criteria for querying data
        """
        return Criterion(self, Criterion.SIMPLE_OPERATORS.GT, other)

    def __ge__(self, other):
        """
        Overriding the <= operator
        :param other: a value for fetching data
        :return:  a new Criterion object representing the criteria for querying data
        """
        return Criterion(self, Criterion.SIMPLE_OPERATORS.GTE, other)

    # def _in(self, _list):
    #     if type(_list) is not list:
    #         raise Exception("The comparision value should be a list.")
    #
    #     return Criterion(self, Criterion.SIMPLE_OPERATORS.IN, _list)
    #
    # def _not_in(self, _list):
    #     if type(_list) is not list:
    #         raise Exception("The comparision value should be a list.")
    #     return Criterion(self, Criterion.SIMPLE_OPERATORS.NOT_IN, _list)

    def is_null(self):
        """
        Handle the IS_NULL query operation in ContactHub
        :return: a new Criterion object representing the criteria for querying data
        """
        return Criterion(self, Criterion.SIMPLE_OPERATORS.IS_NULL)

    def is_not_null(self):
        """
        Handle the IS_NOT_NULL query operation in ContactHub
        :return:  a new Criterion object representing the criteria for querying data
        """
        return Criterion(self, Criterion.SIMPLE_OPERATORS.IS_NOT_NULL)