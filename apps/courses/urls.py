from django.urls import path

from . import views


urlpatterns = [
    path(
        '<slug:slug>/',
        views.course_detail,
        name='course_detail'
    ),
    path('', views.courses, name='courses'),

]