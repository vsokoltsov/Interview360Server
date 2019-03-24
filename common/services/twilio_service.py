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

        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
        if not self.account_sid and not self.auth_token:
            logging.warning(WARNING_MESSAGE)
            return
        self.client = Client(self.account_sid, self.auth_token)

    def phone_lookup(self, phone):
        """ Verify the give phone number. """
        if not self.account_sid and not self.auth_token:
            logging.warning(WARNING_MESSAGE)
            return

        try:
            self.client.lookups.phone_numbers(phone).fetch()
            return True
        except TwilioRestException:
            return False
