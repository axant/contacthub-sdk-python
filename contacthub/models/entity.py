from contacthub.models.entity_field import EntityField


class Entity(type):

    def __getattr__(self, item):
        return EntityField(self, item)
