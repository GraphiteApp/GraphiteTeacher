from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, './ClassMonitor/index.html')


def login(request):
    if request.method == 'POST':
        print(request.POST['username'])
        print(request.POST['password'])
        return HttpResponse("Logged in")

    return render(request, './ClassMonitor/login.html')
