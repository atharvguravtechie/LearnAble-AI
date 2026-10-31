from django.urls import path
from .views import AITeacherAPIView

urlpatterns = [
    path("ask/", AITeacherAPIView.as_view(), name="ai_teacher_ask"),
]