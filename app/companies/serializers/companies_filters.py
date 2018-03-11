from . import serializers, Company, CompanyMember

class CompaniesFilter(serializers.Serializer):
    """ Serializer for companies filters data """

    roles = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()

    ORDERS = (
        ('employees_count', 'Employees count'),
        ('interviews_count', 'Interviews count'),
        ('vacancies_count', 'Vacancies count')
    )

    def get_roles(self, obj):
        """ Receive dict of the roles """

        return [
            {'title': val, 'key': key } for key, val in CompanyMember.ROLES
        ]

    def get_order(self, obj):
        """ Receive of the possible orders """


        return [
            {'title': val, 'key': key } for key, val in self.ORDERS
        ]
