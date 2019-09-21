from django.db import models
from django.contrib.auth.models import User


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=50)
    operands = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    result = models.CharField(max_length=20)
