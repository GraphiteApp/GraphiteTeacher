from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Profile


class Calculator:
    isAllowed = False
    name = ''

    def __init__(self, name, is_allowed):
        self.name = name
        self.isAllowed = is_allowed

    @staticmethod
    def get_calculators(class_code):
        profile = Profile.objects.get(classCode=class_code)
        return [
            Calculator('Basic', profile.basic_calculator),
            Calculator('Scientific', profile.scientific_calculator),
            Calculator('Graphing', profile.graphing_calculator),
        ]

    @staticmethod
    def update_calculators(user, calculators):
        for calculator in calculators:
            profile = Profile.objects.get(user=user)
            if calculator.name == 'Graphing':
                profile.graphing_calculator = calculator.isAllowed
            elif calculator.name == 'Scientific':
                profile.scientific_calculator = calculator.isAllowed
            elif calculator.name == 'Basic':
                profile.basic_calculator = calculator.isAllowed
            profile.save()

    @staticmethod
    def reset_calculators(user):
        profile = Profile.objects.get(user=user)
        profile.basic_calculator = False
        profile.scientific_calculator = False
        profile.graphing_calculator = False
        profile.save()

    @staticmethod
    def get_allowed_calculators(class_code):
        profile = Profile.objects.get(classCode=class_code)
        return {
            'basic': profile.basic_calculator,
            'scientific': profile.scientific_calculator,
            'graphing': profile.graphing_calculator,
        }


def check_login(request):
    return request.user.is_authenticated


def exam_started(user):
    return Profile.objects.get(user=user).examStarted
