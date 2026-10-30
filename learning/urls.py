from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.subject_list, name='home'),

    path(
        'subject/<int:subject_id>/',
        views.topic_list,
        name='topics'
    ),

    path(
        'lesson/<int:lesson_id>/',
        views.lesson_detail,
        name='lesson_detail'
    ),
]