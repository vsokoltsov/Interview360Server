from .models import Resume
from common.services.twilio_service import TwilioService

twilio = TwilioService()

def resume_exist(field, value, error):
    """ Check wheter or not resume exist """

    try:
        resume = Resume.objects.get(id=value)
    except Resume.DoesNotExist:
        error(field, 'Does not exist')

def phone_validation(field, value, error):
    """ Check whether or not this phone exist """

    if not twilio.phone_lookup(value):
        error(field, 'Is not valid')
