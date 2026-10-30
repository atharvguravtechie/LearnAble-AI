from django.db import models
from django.contrib.auth.models import User
from learning.models import Subject, Topic


class StudentDoubt(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('answered', 'Answered'),
        ('resolved', 'Resolved'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='doubts'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doubts'
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doubts'
    )

    question = models.TextField()

    answer = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - Doubt"