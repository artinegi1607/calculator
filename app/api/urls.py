from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CalculateAPI, ReportAPI

urlpatterns = [
    path('calculate', CalculateAPI.as_view(), name='calculate'),
    path('report', ReportAPI.as_view(), name='report')
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'xml'])
