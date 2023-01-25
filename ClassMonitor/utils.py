from django.shortcuts import redirect
from django.contrib.auth.models import User


def check_login(request):
    return request.user.is_authenticated
