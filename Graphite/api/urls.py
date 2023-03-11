from django.urls import path

from . import views

urlpatterns = [
    path('join_exam', views.join_exam, name='join_exam'),
    path('leave_exam', views.leave_exam, name='leave_exam'),
    path('get_resources', views.get_resources, name='get_resources'),
    path('get_exam_data', views.get_exam_data, name='get_exam_data'),
    path('remove_student', views.remove_student, name='remove_student'),
    path('toggle_resource', views.toggle_resource, name='toggle_resource'),
]
