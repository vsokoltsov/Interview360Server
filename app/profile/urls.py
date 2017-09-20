from django.conf.urls import url
from django.conf.urls import include

from .views import ProfileAPIView
from rest_framework_nested import routers

urlpatterns = [
    url(r'v1/profile', ProfileAPIView.as_view() )
]
