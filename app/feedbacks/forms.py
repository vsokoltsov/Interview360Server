from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from feedbacks.models import Feedback
from common.forms import BaseForm, FormException

import ipdb


class FeedbackForm(BaseForm):
    """
    Feedback form object
    :param id: Identifier of feedback
    :param user_id: Identifier of user who performs feedback
    :param object_id: Identifier of the object, on which feedback is performed
    :param content_type: String represnetation of the model, on which
                         feedback is performed
    :param description: Actual description of the feedback
    """

    schema = {
        'id': {
            'type': 'integer',
            'required': False
        },
        'user_id': {
            'type': 'integer',
            'required': True,
            'empty': False
            # 'not_equal_generic_type': ['object_id', 'content_type']
        },
        'company_id': {
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'object_id': {
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'content_type': {
            'type': 'string',
            'required': True,
            'empty': False,
            'allowed': ['interviews.interview', 'authorization.user']
        },
        'description': {
            'type': 'string',
            'required': True,
            'empty': False,
        }
    }

    def submit(self):
        """ Save feedback information into database """

        if not self.is_valid():
            return False

        try:
            with transaction.atomic():
                self.params['content_type'] = self._get_content_type_provider()
                if not self.obj:
                    self.obj = Feedback.objects.create(**self.params)
                else:
                    self._set_attributes()
                    self.obj.save()
                return True
        except BaseException:
            return False

    def _get_content_type_provider(self):
        """ Receive a correct content type value """

        app_name, model = self.params.get('content_type').split('.')
        content_type = ContentType.objects.get(
            app_label=app_name, model=model
        )
        return content_type

    def _set_attributes(self):
        """ Set attributes to new feedback instance """

        for field, value in self.params.items():
            setattr(self.obj, field, value)
