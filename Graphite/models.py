from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    username = models.CharField(max_length=20, unique=True, null=False, blank=False)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=False, blank=False)
    classCode = models.CharField(max_length=10, unique=True, null=False, blank=False)
    examStarted = models.BooleanField(default=False)
    students = models.ManyToManyField(Student, blank=True)
    left_students = models.ManyToManyField(Student, blank=True, related_name='left_students')
    basic_calculator = models.BooleanField(default=False)
    scientific_calculator = models.BooleanField(default=False)
    graphing_calculator = models.BooleanField(default=False)
