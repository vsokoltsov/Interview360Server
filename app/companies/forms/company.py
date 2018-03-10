from common.forms import BaseForm
from django.db import transaction
from authorization.models import User
from companies.models import CompanyMember
from attachments.models import Image
from profiles.index import UserIndex
from companies.index import CompanyIndex
import ipdb

def owner_exist(field, value, error):
    """ Check whether or not owner exist """

    try:
        user = User.objects.get(id=value)
    except User.DoesNotExist:
        error(field, 'Does not exist')

class CompanyForm(BaseForm):
    """ Form object for company model """

    schema = {
        'name': {
            'type': 'string',
            'empty': False,
            'required': True
        },
        'start_date': {
            'type': 'string',
            'regex': '^\d{4}-\d{2}-\d{2}$',
            'empty': False,
            'required': True
        },
        'description': {
            'type': 'string',
            'empty': True,
            'required': False
        },
        'city': {
            'type': 'string',
            'empty': False,
            'required': True
        },
        'owner_id': {
            'type': 'integer',
            'empty': False,
            'required': True,
            'validator': owner_exist
        },
        'current_user': {
            'empty': False,
            'required': True
        },
        'attachment': {
            'required': False,
            'type': 'dict',
            'schema': {
                'id': {
                    'type': 'integer',
                    'required': True,
                    'empty': False
                }
            }
        }
    }

    def submit(self):
        """ Set attributes to the company instance and save to the database """

        if not self.is_valid(): return False

        try:
            with transaction.atomic():
                attachment_json = self.params.pop('attachment', None)
                new_company = not self.obj.id
                self._set_attributes()
                self.obj.save()
                if new_company:
                    company_member = CompanyMember.objects.create(
                        company_id=self.obj.id, user_id=self.current_user.id,
                        role=CompanyMember.COMPANY_OWNER, active=True
                    )
                self._set_attachment(attachment_json)
                UserIndex.store_index(User.objects.get(
                    id=self.params.get('owner_id'))
                )
                CompanyIndex.store_index(self.obj)
                return True
        except Exception as e:
            return False

    def is_valid(self):
        """ Override the parent class method """

        result = super(CompanyForm, self).is_valid()
        if not result:
            return result

        if self.obj.id:
            not_belongs_to_company = not self.is_company_member
            not_allowed_to_edit = not_belongs_to_company and not self.is_allowed_to_update

            if not_belongs_to_company:
                self.set_error_message(
                    'company_member', 'Does not belong to company'
                )
                result = False

            if not_allowed_to_edit:
                self.set_error_message(
                    'company_member', 'is not allowed to edit company'
                )
                result = False
        return result

    def _set_attributes(self):
        for field, value in self.params.items():
            setattr(self.obj, field, value)

    def _set_attachment(self, attachment_json):
        """ Set attachment to the company's instance """

        if attachment_json:
            attachment_id = attachment_json.get('id')
            attachment = Image.objects.get(id=attachment_id)
            attachment.object_id=self.obj.id
            attachment.save()
            return attachment

    @property
    def is_company_member(self):
        """ Wrapper for validation function """

        return self._is_company_member(self.obj.id, self.current_user.id)

    @property
    def is_allowed_to_update(self):
        """ Wrapper for validation function """

        return self._is_allowed_to_update(self.obj.id, self.current_user.id)

    def _is_company_member(self, company_id, user_id):
        """ Check whether or not the current user is the member of the company """

        try:
            CompanyMember.objects.get(company_id=company_id, user_id=user_id)
            return True
        except CompanyMember.DoesNotExist:
            return False

    def _is_allowed_to_update(self, company_id, user_id):
        """ Check whether or not the current user is allowed to edit company """

        try:
            company_member = CompanyMember.objects.get(company_id=company_id, user_id=user_id)
            return company_member.role == CompanyMember.COMPANY_OWNER
        except CompanyMember.DoesNotExist:
            return False
