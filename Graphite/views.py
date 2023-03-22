from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from . import utils
from . import models
import random
import urllib.parse


def index(request):
    loggedIn = utils.check_login(request)

    if loggedIn:
        exam_started = utils.exam_started(request.user)
    else:
        exam_started = False

    if request.method == 'POST':
        models.Profile.objects.filter(user=request.user).update(examStarted=True)
        # redirect to exam
        return redirect('/exam')

    return render(request, './Graphite/index.html', {
        'user': request.user,
        'exam_started': exam_started,
        'is_logged_in': loggedIn,
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
    return redirect('/')


def exam(request):
    isLoggedIn = utils.check_login(request)
    if not isLoggedIn:
        return redirect('login')

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
        'is_logged_in': isLoggedIn,
    })


def exam_video(request):
    isLoggedIn = utils.check_login(request)
    if not isLoggedIn:
        return redirect('login')

    # if not exam started, redirect to exam
    if not utils.exam_started(request.user):
        return redirect('/exam')

    return render(request, './Graphite/exam_video.html', {
        "rowNum": range(1, 3),
        "columnNum": range(1, 6),
        'is_logged_in': isLoggedIn,
    })


def add_resource(request):
    isLoggedIn = utils.check_login(request)
    if not isLoggedIn:
        return redirect('login')

    classCode = models.Profile.objects.get(user=request.user).classCode

    if request.method == 'POST':
        resourceName = request.POST['name']
        resourceURL = request.POST['url']
        oldResourceName = request.POST['old_name']

        if oldResourceName != '':
            # delete old resource
            utils.Resource.delete_resource(oldResourceName)

        # add new resource
        utils.Resource.add_resource(classCode, resourceName, resourceURL)

        return redirect('/exam')

    # check if resource param is in request
    resourceName = request.GET.get('resource', '')

    resources = utils.Resource.get_resources(models.Profile.objects.get(user=request.user).classCode)

    resource = {
        'name': resourceName,
        'URL': ''
    }

    # check if resource is valid
    if resourceName in [resource['name'] for resource in resources]:
        resource['URL'] = utils.Resource.get_resource(resourceName)['url']

    return render(request, './Graphite/add_resource.html', {
        'resource': resource,
        'is_logged_in': isLoggedIn,
        'exam_started': utils.exam_started(request.user),
    })
