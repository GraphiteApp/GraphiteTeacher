from django.urls import path

from . import views

urlpatterns = [
    path('join_exam', views.join_exam, name='join_exam'),
    path('leave_exam', views.leave_exam, name='leave_exam'),
    path('get_calculators', views.get_calculators, name='get_calculators'),
    path('get_exam_data', views.get_exam_data, name='get_exam_data'),
]
