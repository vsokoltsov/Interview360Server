from rest_framework import serializers
from authorization.models import User
from attachments.serializers import AttachmentBaseSerializer

from .current_user import CurrentUserSerializer
from .user import UserSerializer
