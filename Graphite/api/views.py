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

        # add student to students
        teacher.students.add(Student.objects.get(username=username))

        response.status_code = 200
        response.content = 'Joined exam'
        return response

    return HttpResponse('Invalid request method')


@csrf_exempt
def get_calculators(request):
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
        response.content = json.dumps(utils.Calculator.get_allowed_calculators(class_code))
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

        if student.teacher is not teacher.user:
            response.status_code = 400
            response.content = 'Student is not in this exam'
            return response

        # add student to left_students
        Profile.objects.get(classCode=class_code).left_students.add(student)

        print(student.teacher)

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

        # return exam students, allowed_calculators, and exam_started
        response = HttpResponse()

        # get classCode from user
        class_code = Profile.objects.get(user=request.user).classCode

        # get student from teacher sorted by username
        students = Profile.objects.get(classCode=class_code).students.all().order_by('username')
        students = [student.username for student in students]

        # get allowed calculators
        allowed_calculators = utils.Calculator.get_allowed_calculators(class_code)

        # get exam started
        exam_started = Profile.objects.get(user=request.user).examStarted

        # return json
        response.status_code = 200
        response.content = json.dumps({
            'students': students,
            'allowed_calculators': allowed_calculators,
            'exam_started': exam_started
        })

        return response

    return HttpResponse('Invalid request method')
