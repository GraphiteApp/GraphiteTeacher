from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=False, blank=False)
    classCode = models.CharField(max_length=10, unique=True, null=False, blank=False)
