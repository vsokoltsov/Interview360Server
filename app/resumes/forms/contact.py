import re

from django.db.utils import IntegrityError

import ipdb

from . import  (
    BaseForm, FormException, cerberus, Resume, Workplace, Company, Contact,
    transaction, WorkplaceForm, resume_exist
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
            'regex': '\A(\+)[0-9]{7,12}'
        },
        'phone_comment': {
            'type': 'string',
            'required': False,
            'empty': True
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
                    for key, value in self.params.items():
                        setattr(self.obj, key, value)
                    self.obj.save()
                    return True
        except IntegrityError as e:
            self._set_uniq_errors(str(e))
            return False

    def _set_uniq_errors(self, e):
        """ Set unique index errors into the form errors """
        for item in ['email', 'phone']:
            if re.search(item, e):
                self.errors[item] = ['Is not unique']
