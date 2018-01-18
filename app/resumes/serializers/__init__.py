from rest_framework import serializers
from resumes.models import Resume
from authorization.models import User
from vacancies.fields import SkillsField
from common.serializers.user_serializer import UserSerializer
from common.fields import CustomField
from resumes.index import ResumesIndex

from .resumes import ResumesSerializer
from .resume import ResumeSerializer
