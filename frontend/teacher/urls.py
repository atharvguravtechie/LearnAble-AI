
from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('', views.home, name='home'),
    path('record-activity/', views.record_activity, name='record_activity'),
]
