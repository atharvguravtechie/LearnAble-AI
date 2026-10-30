
from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.home, name='home'),
    path('take/', views.take_quiz, name='take_quiz'),
]
