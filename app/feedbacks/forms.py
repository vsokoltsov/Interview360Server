from common.forms import BaseForm, FormException

class FeedbackForm:
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
        'object_id': {
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'content_type': {
            'type': 'string',
            'required': True,
            'empty': False,
            'oneof': [ 'interviews.interview', 'authorization.user' ]
        },
        'description': {
            'type': 'string',
            'required': True,
            'empty': False,
        }
    }

    def submit(self):
        """ Save feedback information into database """
        pass
