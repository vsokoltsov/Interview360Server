from common.forms import BaseForm
import cerberus
from resumes.models import Resume, Workplace
from companies.models import Company
from django.db import transaction

from .workplace import WorkplaceForm
