from contacthub.models.customer_properties.property import Property


class Education(Property):
    """
    Education model
    """
    class SCHOOL_TYPES:
        """
        Subclasses with school types for the schoolType field of Education
        """
        PRIMARY_SCHOOL = 'PRIMARY_SCHOOL'
        SECONDARY_SCHOOL = 'SECONDARY_SCHOOL'
        HIGH_SCHOOL = 'HIGH_SCHOOL'
        COLLEGE = 'COLLEGE'
        OTHER = 'OTHER'
