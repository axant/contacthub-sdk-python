from contacthub.models.query.entity_field import EntityField


class EntityMeta(type):

    def __getattr__(self, item):
        return EntityField(self, item)
