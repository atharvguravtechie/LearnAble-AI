from django.urls import path
from . import views

app_name = 'doubts'

urlpatterns = [
    path('', views.home, name='home'),
]