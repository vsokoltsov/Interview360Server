import os
import logging

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

WARNING_MESSAGE = 'Credentials for Twilio are empty. In order to user Twilio,\
                    please provide TWILIO_ACCOUNT_SID and \
                    TWILIO_AUTH_TOKEN environment variables'


class TwilioService:
    """Base twilio service."""

    def __init__(self):
        """ Initialize twilio service; Instanciate Client object. """

        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.client = Client(account_sid, auth_token)
        if not account_sid and not auth_token:
            logging.warning(WARNING_MESSAGE)

    def phone_lookup(self, phone):
        """ Verify the give phone number. """

        try:
            self.client.lookups.phone_numbers(phone).fetch()
            return True
        except TwilioRestException:
            return False
