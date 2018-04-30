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

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

import ipdb


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)
        doc = coreapi.Document(
            title='Companies API',
            content = {
                'companies': {
                    'list': coreapi.Link(
                        url='/companies',
                        action='get',
                        description='Return list of companies for current user'
                    ),
                    'create': coreapi.Link(
                        url='/companies',
                        action='post',
                        description='Create new company',
                        fields=[
                            coreapi.Field(
                                'name',
                                required=True,
                                location="form",
                                description='Company\'s name',
                                schema=coreschema.String()
                            ),
                            coreapi.Field(
                                'description',
                                required=True,
                                location="form",
                                description='Company\'s description',
                                schema=coreschema.String()
                            ),
                            coreapi.Field(
                                'start_date',
                                required=True,
                                location="form",
                                description='Company\'s start_date',
                                schema=coreschema.String()
                            ),
                        ]
                    )
                }
            }
        )

        return Response(doc)

# schema_view = get_swagger_view(title='Interview360 API')




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('authorization.urls')),
    url(r'^api/', include('companies.urls')),
    url(r'^api/', include('skills.urls')),
    url(r'^api/', include('feedbacks.urls')),
    url(r'^api/', include('profiles.urls')),
    url(r'^api/', include('attachments.urls')),
    url(r'^api/', include('resumes.urls')),
    url(r'^docs/v1/', SwaggerSchemaView.as_view())
]

SILK_ENABLED = os.environ.get("SILK_ENABLED")

if settings.DEBUG and SILK_ENABLED:
    urlpatterns += [
        url(r'^silk/', include('silk.urls', namespace='silk'))
    ]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
init_indexes()
