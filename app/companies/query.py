import re
from decimal import Decimal

from django.db.models import Count
from companies.models import Company, CompanyMember

class CompaniesQuery:
    """ Query class for Company """

    def __init__(self, params, current_user):
        """ Constructor; Set parameters and current user """

        self.params = params
        self.current_user = current_user

    def list(self):
        """ Perform query for extracting list of the Company instances """

        queryset = self.current_user.companies.prefetched_list()
        return queryset

    @property
    def role(self):
        """ Return value of the role """
        pass

    @property
    def order(self):
        """ Return value of the order """
        pass
