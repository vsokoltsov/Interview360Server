import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import ipdb


class TwilioService:
    """Base twilio service."""

    def __init__(self):
        """Initialize twilio service; Instanciate Client object."""

        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.client = Client(account_sid, auth_token)

    def phone_lookup(self, phone):
        """Verify the give phone number."""

        try:
            self.client.lookups.phone_numbers(phone).fetch()
            return True
        except TwilioRestException:
            return False
