from django.http import HttpResponse
from ..models import *
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def join_exam(request):
    if request.method == 'POST':
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
        if teacher.students.exists() and username in teacher.students:
            response.status_code = 400
            response.content = 'Student already exists'
            return response

        # add student to students
        Student.objects.create(username=username, teacher=teacher.user).save()

        # add student to students
        teacher.students.add(Student.objects.get(username=username))

        response.status_code = 200
        response.content = 'Joined exam'
        return response

    return HttpResponse('Invalid request method')