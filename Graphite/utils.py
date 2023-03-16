from django.shortcuts import redirect
from django.contrib.auth.models import User
from . import models


class Resource:
    isAllowed = False
    name = ''

    def __init__(self, name, is_allowed, url):
        self.name = name
        self.isAllowed = is_allowed

    @staticmethod
    def get_resources(class_code):
        profile = models.Profile.objects.get(classCode=class_code)
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
            profile = models.Profile.objects.get(user=user)
            if resource.isAllowed:
                profile.allowed_resources.add(resource)
                profile.disabled_resources.remove(resource)
            else:
                profile.allowed_resources.remove(resource)
                profile.disabled_resources.add(resource)

            profile.save()

    @staticmethod
    def disable_resources(user):
        profile = models.Profile.objects.get(user=user)
        for resource in Resource.get_resources(profile.classCode):
            resourceObj = models.Resource.objects.get(name=resource['name'])
            profile.allowed_resources.remove(resourceObj)
            profile.disabled_resources.add(resourceObj)

        profile.save()

    @staticmethod
    def toggle_resource(class_code, resource_name, is_enable):
        profile = models.Profile.objects.get(classCode=class_code)
        resource = models.Resource.objects.get(name=resource_name)

        if is_enable:
            profile.allowed_resources.add(resource)
            if resource in profile.disabled_resources.all():
                profile.disabled_resources.remove(resource)
        else:
            profile.disabled_resources.add(resource)
            if resource in profile.allowed_resources.all():
                profile.allowed_resources.remove(resource)

        profile.save()

    @staticmethod
    def delete_resource_from_profile(class_code, resource_name):
        profile = models.Profile.objects.get(classCode=class_code)
        resource = models.Resource.objects.get(name=resource_name)

        profile.allowed_resources.remove(resource)
        profile.disabled_resources.remove(resource)

        profile.save()

    @staticmethod
    def get_resource(resource_name):
        resource = models.Resource.objects.get(name=resource_name)
        return {
            'name': resource.name,
            'url': resource.url
        }

    @staticmethod
    def add_resource(class_code, resource_name, url):
        models.Resource.objects.create(name=resource_name, url=url)

        profile = models.Profile.objects.get(classCode=class_code)
        resource = models.Resource.objects.get(name=resource_name)

        profile.allowed_resources.add(resource)
        profile.save()

    @staticmethod
    def delete_resource(resource_name):
        models.Resource.objects.get(name=resource_name).delete()


def check_login(request):
    return request.user.is_authenticated


def exam_started(user):
    return models.Profile.objects.get(user=user).examStarted


def start_exam(user):
    models.Profile.objects.filter(user=user).update(examStarted=True)

    # add default resources as disabled
    profile = models.Profile.objects.get(user=user)

    resources = {
        'Graphing Calculator': 'https://www.desmos.com/calculator',
        'Scientific Calculator': 'https://www.desmos.com/scientific',
        'Basic Calculator': 'https://www.desmos.com/fourfunction',
        'Periodic Table': 'https://ptable.com/#Properties'
    }

    for name, url in resources.items():
        # either create or get the resource, depending on if it already exists
        if models.Resource.objects.filter(name=name).exists():
            resource = models.Resource.objects.get(name=name)
        else:
            resource = models.Resource(name=name, url=url)
            resource.save()

        profile.disabled_resources.add(resource)
