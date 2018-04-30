"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .settings import MEDIA_URL, MEDIA_ROOT
from common.indexes.base import init_indexes
from rest_framework.renderers import CoreJSONRenderer
from rest_framework_swagger.views import get_swagger_view
import coreapi
import coreschema
from openapi_codec import encode

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
import yaml
import ipdb

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('authorization.urls')),
    url(r'^api/', include('companies.urls')),
    url(r'^api/', include('skills.urls')),
    url(r'^api/', include('feedbacks.urls')),
    url(r'^api/', include('profiles.urls')),
    url(r'^api/', include('attachments.urls')),
    url(r'^api/', include('resumes.urls'))
]

SILK_ENABLED = os.environ.get("SILK_ENABLED")

if settings.DEBUG and SILK_ENABLED:
    urlpatterns += [
        url(r'^silk/', include('silk.urls', namespace='silk'))
    ]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
init_indexes()
