from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ObtainToken

urlpatterns = [
    path('create_token', ObtainToken.as_view(), name='create-token')
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'xml'])
