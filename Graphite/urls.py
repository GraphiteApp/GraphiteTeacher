# urls for Graphite

from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_page, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_page, name='logout'),
    path('exam', views.exam, name='exam'),
    path('exam_video', views.exam_video, name='exam_video'),
    path('add_resource', views.add_resource, name='add_resource'),
    path('settings', views.settings, name='settings'),
    path('', views.index, name='index'),
]
