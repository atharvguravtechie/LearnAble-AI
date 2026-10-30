from django.db import models
from django.contrib.auth.models import User
from learning.models import Subject, Topic


class StudentNote(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='study_notes'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='student_notes'
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_notes'
    )

    title = models.CharField(max_length=200)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title