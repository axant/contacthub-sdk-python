from contacthub.models.base_property import BaseProperty


class Education(BaseProperty):
    class SCHOOL_TYPES:
        PRIMARY_SCHOOL = 'PRIMARY_SCHOOL'
        SECONDARY_SCHOOL = 'SECONDARY_SCHOOL'
        HIGH_SCHOOL = 'HIGH_SCHOOL'
        COLLEGE = 'COLLEGE'
        OTHER = 'OTHER'
