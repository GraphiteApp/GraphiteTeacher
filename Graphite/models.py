from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    username = models.CharField(max_length=20, unique=True, null=False, blank=False)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)


class Resource(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False, blank=False)
    url = models.CharField(max_length=100, unique=True, null=False, blank=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=False, blank=False)
    classCode = models.CharField(max_length=10, unique=True, null=False, blank=False)
    examStarted = models.BooleanField(default=False)
    students = models.ManyToManyField(Student, blank=True)
    left_students = models.ManyToManyField(Student, blank=True, related_name='left_students')
    allowed_resources = models.ManyToManyField(Resource, blank=True, related_name='allowed_resources')
    disabled_resources = models.ManyToManyField(Resource, blank=True, related_name='disabled_resources')
