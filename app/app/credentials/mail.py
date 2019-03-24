import os

MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
MAILGUN_SERVER_NAME = os.environ.get('MAILGUN_SERVER_NAME')
DEFAULT_FROM_MAIL = "you@example.com"

if MAILGUN_API_KEY and MAILGUN_SERVER_NAME:
    ANYMAIL = {
        "MAILGUN_API_KEY": MAILGUN_API_KEY,
        "MAILGUN_SERVER_NAME": MAILGUN_SERVER_NAME
    }
    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
