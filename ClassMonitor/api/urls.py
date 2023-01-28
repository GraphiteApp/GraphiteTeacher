from django.urls import path

from . import views

urlpatterns = [
    path('join_exam', views.join_exam, name='join_exam'),
    path('get_calculators', views.get_calculators, name='get_calculators'),
]
