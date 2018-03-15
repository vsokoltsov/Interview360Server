import re
from decimal import Decimal

from common.queries import BaseQuery, QueryOrderMixin
from django.db.models import Count
from companies.models import Company, CompanyMember

class CompaniesQuery(BaseQuery, QueryOrderMixin):
    """ Query class for Company """

    order_fields = [k for k, _ in Company.ORDER_FIELDS]

    def __init__(self, params, current_user):
        """ Constructor; Set parameters and current user """

        self.params = params
        self.current_user = current_user

    def list(self):
        """ Perform query for extracting list of the Company instances """

        queryset = self.current_user.companies.prefetched_list()

        if self.role:
            queryset = queryset.filter(
                companymember__user_id=self.current_user.id,
                companymember__role=self.role
            )

        if self.order:
            queryset = queryset.order_by(self.order)

        return queryset

    @property
    def role(self):
        """ Return value of the role """

        role = self.params.get('role')
        return role if self._is_valid_role(role) else None

    @property
    def roles(self):
        """ Return list of roles for the validation of role """

        return [k for k, _ in CompanyMember.ROLES]

    def _is_valid_role(self, role):
        """ Check whether or not the role is valid """

        return role in self.roles
