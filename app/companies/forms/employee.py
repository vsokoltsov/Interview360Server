from common.forms import BaseForm
from django.db import transaction
from authorization.models import User
from companies.models import Company, CompanyMember
from companies.validators import company_exist
from common.schemas import EMAIL_SCHEMA


class EmployeeForm(BaseForm):
    """
    Form object for employees creation.

    :param company_id: Identifier of the company
    :param employees: List of employees' data
    """

    schema = {
        'company_id': {
            'type': 'integer',
            'empty': False,
            'required': True,
            'validator': company_exist
        },
        'employees': {
            'type': 'list',
            'empty': False,
            'required': True,
            'schema': {
                'type': 'dict',
                'schema': {
                    'email': EMAIL_SCHEMA,
                    'role': {
                        'type': 'integer',
                        'empty': False,
                        'required': True,
                        'allowed': [role[0] for role in CompanyMember.ROLES]
                    }
                }
            }
        }
    }
