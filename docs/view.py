from rest_framework.views import APIView
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework_swagger import renderers
from rest_framework.response import Response

from docs.v1 import documentation


class SwaggerSchemaView(APIView):
    """Swagger view for application's documentation."""

    permission_classes = [AllowAny]
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        """Receive documentation information."""

        return Response(documentation)
