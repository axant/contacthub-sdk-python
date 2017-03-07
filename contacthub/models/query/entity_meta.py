from contacthub.models.query.entity_field import EntityField


class EntityMeta(type):
    """Metaclass for defining an Entity.

    Use this metaclass to handling the __getattr__ method and returns a new EntityField.
    This metaclass is useful for creating query objects and optimize the querying syntax.
    """

    class Enitites:
        """
        Subclass for queryable entity in ContactHub
        """
        CUSTOMERS = 'customers'

    def __getattr__(self, item):
        """
        If you call Entity.field, this function create a new EntityField object with an entity and the requested item
        :param item: the property that we want to query
        :return: a new EntityField object for queries
        """
        return EntityField(self, item)
