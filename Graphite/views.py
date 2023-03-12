from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from . import utils
from . import models
import random
import urllib.parse


resources = [
    'Basic',
    'Scientific',
    'Graphing',
]


def index(request):
    if not utils.check_login(request):
        return redirect('login')

    if request.method == 'POST':
        models.Profile.objects.filter(user=request.user).update(examStarted=True)
        # redirect to exam
        return redirect('/exam')

    return render(request, './Graphite/index.html', {
        'class_code': models.Profile.objects.get(user=request.user).classCode if models.Profile.objects.filter(
            user=request.user).exists() else "no class code",
        'user': request.user,
        'exam_started': utils.exam_started(request.user),
    })


def login_page(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is not None:
            login(request, user)
            return redirect('index')

        return HttpResponse('Invalid username or password')

    return render(request, './Graphite/login.html')


def register(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        ).save()

        # generate unique class code
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        while True:
            class_code = ''
            for i in range(10):
                class_code += alphabet[random.randrange(0, 26)]
            # check if class code is unique
            if not models.Profile.objects.filter(classCode=class_code).exists():
                break

        models.Profile(
            user=User.objects.get(username=request.POST['username']),
            classCode=class_code
        ).save()

        return redirect('login')

    return render(request, './Graphite/register.html')


def logout_page(request):
    logout(request)
    return redirect('login')


def exam(request):
    if not utils.check_login(request):
        return redirect('login')

    global resources

    user = request.user
    profile = models.Profile.objects.get(user=user)

    # check if exam has started
    if not models.Profile.objects.get(user=request.user).examStarted:
        # start exam
        utils.start_exam(user)

    # probably a better way to do this
    userResources = utils.Resource.get_resources(profile.classCode)

    if request.method == 'POST':
        request_type = request.POST['type']
        if request_type == 'end_exam':
            models.Profile.objects.filter(user=user).update(examStarted=False)
            # clear students
            models.Profile.objects.get(user=user).students.clear()
            models.Student.objects.filter(teacher=user).delete()

            # clear left_students
            models.Profile.objects.get(user=user).left_students.clear()

            # clear resources
            utils.Resource.disable_resources(user)
            return redirect('/')

        if request_type == 'update_resources':
            for resource in userResources:
                resource.isAllowed = resource.name in request.POST

            utils.Resource.update_resources(user, userResources)

    return render(request, './Graphite/exam.html', {
        'class_code': models.Profile.objects.get(user=user).classCode if models.Profile.objects.filter(
            user=user).exists() else "no class code",
        'resources': userResources,
        'exam_started': True,
    })


def exam_video(request):
    if not utils.check_login(request):
        return redirect('login')

    # if not exam started, redirect to exam
    if not utils.exam_started(request.user):
        return redirect('/exam')

    return render(request, './Graphite/exam_video.html', {
        "rowNum": range(1, 3),
        "columnNum": range(1, 6),
    })
