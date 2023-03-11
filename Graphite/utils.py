from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Profile


class Resource:
    isAllowed = False
    name = ''

    def __init__(self, name, is_allowed, url):
        self.name = name
        self.isAllowed = is_allowed

    @staticmethod
    def get_resources(class_code):
        profile = Profile.objects.get(classCode=class_code)
        resources = []

        for resource in profile.allowed_resources.all():
            resources.append({
                'name': resource.name,
                'url': resource.url,
                'isAllowed': True
            })

        for resource in profile.disabled_resources.all():
            resources.append({
                'name': resource.name,
                'url': resource.url,
                'isAllowed': False
            })

        return resources

    @staticmethod
    def update_resources(user, resources):
        for resource in resources:
            profile = Profile.objects.get(user=user)
            if resource.isAllowed:
                profile.allowed_resources.add(resource)
                profile.disabled_resources.remove(resource)
            else:
                profile.allowed_resources.remove(resource)
                profile.disabled_resources.add(resource)

            profile.save()

    @staticmethod
    def disable_resources(user):
        profile = Profile.objects.get(user=user)
        for resource in Resource.get_resources(profile.classCode):
            profile.allowed_resources.remove(resource)
            profile.disabled_resources.add(resource)

        profile.save()


def check_login(request):
    return request.user.is_authenticated


def exam_started(user):
    return Profile.objects.get(user=user).examStarted
