import re

from django.db.utils import IntegrityError

import ipdb

from . import (
    BaseForm, FormException, cerberus, Resume, Workplace, Company, Contact,
    transaction, WorkplaceForm, resume_exist, phone_validation
)
from common.advisory_lock import advisory_lock


class ContactForm(BaseForm):
    """
    Form for resume's contact information.
    :param resume_id: Resume object link
    :params email: Prefered user email
    :param phone: Prefered phone number
    :param phone_comment: Comment for the phone number
    :param social_networks: key-value store for the social networks
    :return True/False whether or not form was submitted
    """

    schema = {
        'id': {
            'type': 'integer',
            'required': False
        },
        'resume_id': {
            'type': 'integer',
            'empty': False,
            'required': True,
            'validator': resume_exist
        },
        'email': {
            'type': 'string',
            'empty': False,
            'required': True,
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        },
        'phone': {
            'type': 'string',
            'empty': False,
            'required': True,
            'regex': '\A(\+)[0-9]{7,12}',
            'validator': phone_validation
        },
        'phone_comment': {
            'type': 'string',
            'required': False,
            'empty': True,
            'nullable': True
        },
        'social_networks': {
            'type': 'dict',
            'required': False,
            'empty': True
        }
    }

    def submit(self):
        """ Validate form and create contact """

        if not self.is_valid():
            return False

        try:
            resume_id = self.params.get('resume_id')
            with advisory_lock('resume_{}_contact'.format(resume_id)) as acquired:
                with transaction.atomic():
                    contact_id = self.params.get('id')
                    if contact_id:
                        contact = Contact.objects.get(id=contact_id)
                        contact = self._set_attributes(contact)
                    else:
                        contact = Contact.objects.create(**self.params)
                    self.obj = contact
                    return True
        except IntegrityError as e:
            self._set_uniq_errors(str(e))
            return False

    def _set_uniq_errors(self, e):
        """ Set unique index errors into the form errors """

        for item in ['email', 'phone']:
            if re.search(item, e):
                self.errors[item] = ['Is not unique']

    def _set_attributes(self, contact):
        """ Set attributes for the contact """

        for key, value in self.params.items():
            setattr(contact, key, value)
        contact.save()
        return contact
