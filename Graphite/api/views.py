from django.http import HttpResponse
from ..models import *
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from .. import utils
import json


@csrf_exempt
def join_exam(request):
    if request.method == 'POST':
        # check if class_code and username are in request
        if 'class_code' not in request.POST or 'username' not in request.POST:
            response = HttpResponse()
            response.status_code = 400
            response.content = 'Missing class_code or username'
            return response

        # get classCode
        response = HttpResponse()
        class_code = request.POST['class_code']
        # get username
        username = request.POST['username']

        # check if class code exists
        if not Profile.objects.filter(classCode=class_code).exists():
            response.status_code = 404
            response.content = 'Class code does not exist'
            return response

        teacher = Profile.objects.get(classCode=class_code)

        if not teacher.examStarted:
            response.status_code = 400
            response.content = 'Exam has not started'
            return response

        # check if student exists
        if Student.objects.filter(username=username).exists():
            student = Student.objects.get(username=username)
            if student.teacher is not None:
                response.status_code = 400
                response.content = 'Student already exists'
                return response
        else:
            # add student to students
            Student.objects.create(username=username, teacher=teacher.user).save()

        student = Student.objects.get(username=username)

        # if the student has left the same exam, remove them from left_students
        if Profile.objects.filter(classCode=class_code, left_students=student).exists():
            teacher.left_students.remove(student)

        # add student to students
        teacher.students.add(Student.objects.get(username=username))

        teacher.save()

        # add teacher to student
        student.teacher = teacher.user

        student.save()

        response.status_code = 200
        response.content = 'Joined exam'
        return response

    return HttpResponse('Invalid request method')


@csrf_exempt
def get_resources(request):
    if request.method == 'GET':
        # get classCode
        response = HttpResponse()
        class_code = request.GET.get('class_code', None)

        # check if class code exists
        if not Profile.objects.filter(classCode=class_code).exists():
            response.status_code = 404
            response.content = 'Class code does not exist'
            return response

        response.status_code = 200
        response.content = json.dumps(utils.Resource.get_resources(class_code))
        return response

    return HttpResponse('Invalid request method')


@csrf_exempt
def leave_exam(request):
    if request.method == 'POST':
        # get classCode and username
        response = HttpResponse()
        class_code = request.POST['class_code']
        username = request.POST['username']

        # check if class code exists
        if not Profile.objects.filter(classCode=class_code).exists():
            response.status_code = 404
            response.content = 'Class code does not exist'
            return response

        # check if student exists
        if not Student.objects.filter(username=username).exists():
            response.status_code = 404
            response.content = 'Student does not exist'
            return response

        student = Student.objects.get(username=username)
        teacher = Profile.objects.get(classCode=class_code)

        if student.teacher != teacher.user:
            response.status_code = 400
            response.content = 'Student is not in this exam'
            return response

        # add student to left_students
        Profile.objects.get(classCode=class_code).left_students.add(student)

        # remove teacher from student
        student.teacher = None

        student.save()

        # remove student from students
        Profile.objects.get(classCode=class_code).students.remove(student)

        response.status_code = 200
        response.content = 'Left exam'

        return response

    return HttpResponse('Invalid request method')


@csrf_exempt
def get_exam_data(request):
    if request.method == 'GET':
        # if authed
        if not utils.check_login(request):
            return HttpResponse('Not logged in')

        # return exam students, allowed_resources, and exam_started
        response = HttpResponse()

        # get classCode from user
        class_code = Profile.objects.get(user=request.user).classCode

        # get student from teacher sorted by username
        students = Profile.objects.get(classCode=class_code).students.all()
        students = [student.username for student in students]

        # get resources
        resources = utils.Resource.get_resources(class_code)

        # get exam started
        exam_started = Profile.objects.get(user=request.user).examStarted

        # left students
        left_students = [student.username for student in Profile.objects.get(classCode=class_code).left_students.all()]

        # return json
        response.status_code = 200
        response.content = json.dumps({
            'students': students,
            'resources': resources,
            'exam_started': exam_started,
            'left_students': left_students
        })

        return response

    return HttpResponse('Invalid request method')


def remove_student(request):
    if request.method == 'GET':
        return HttpResponse('Invalid request method')

    # if authed
    if not utils.check_login(request):
        return HttpResponse('Not logged in')

    # check if username is in request
    body = json.loads(request.body)
    if 'username' not in body:
        return HttpResponse('Missing username')

    username = body['username']

    if not Student.objects.filter(username=username).exists():
        return HttpResponse('Student does not exist')

    # if student is not in the current user's exam
    if Student.objects.get(username=username).teacher != request.user:
        return HttpResponse('Student is not in this exam')

    # delete student
    Student.objects.get(username=username).delete()

    return HttpResponse('Student removed')


def toggle_resource(request):
    if request.method == 'GET':
        return HttpResponse('Invalid request method')

    # check auth
    if not utils.check_login(request):
        return HttpResponse('Not logged in')

    # check if resource and isEnable are in request
    body = json.loads(request.body)

    if 'resource' not in body:
        return HttpResponse('Missing resource')

    if 'isEnable' not in body:
        return HttpResponse('Missing isEnable')

    if not isinstance(body['isEnable'], bool):
        return HttpResponse('isEnable must be a boolean')

    resource = body['resource']
    is_enable = body['isEnable']

    # check if resource is valid
    resources = utils.Resource.get_resources(Profile.objects.get(user=request.user).classCode)

    # we cannot use in because resources is a list of dicts
    foundResource = False
    for r in resources:
        if r['name'] == resource:
            foundResource = True
            break

    if not foundResource:
        return HttpResponse('Invalid resource')

    # toggle resource
    utils.Resource.toggle_resource(Profile.objects.get(user=request.user).classCode, resource, is_enable)

    return HttpResponse('Resource toggled')


def delete_resource(request):
    if request.method == 'GET':
        return HttpResponse('Invalid request method')

    # check auth
    if not utils.check_login(request):
        return HttpResponse('Not logged in')

    # check if resource is in request
    body = json.loads(request.body)

    if 'resource' not in body:
        return HttpResponse('Missing resource')

    resource = body['resource']

    # check if resource is valid
    resources = utils.Resource.get_resources(Profile.objects.get(user=request.user).classCode)

    # we cannot use in because resources is a list of dicts
    foundResource = False
    for r in resources:
        if r['name'] == resource:
            foundResource = True
            break

    if not foundResource:
        return HttpResponse('Invalid resource')

    # delete resource
    utils.Resource.delete_resource(Profile.objects.get(user=request.user).classCode, resource)

    return HttpResponse('Resource deleted')
