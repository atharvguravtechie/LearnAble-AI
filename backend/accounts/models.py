from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):

    LEARNING_STYLE_CHOICES = [
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('reading', 'Reading and Writing'),
        ('practical', 'Practical Learning'),
        ('mixed', 'Mixed Learning'),
        ('unsure', 'Not Sure'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    education_level = models.CharField(
        max_length=50,
        help_text="School, College, or Other"
    )

    class_or_grade = models.CharField(
        max_length=50,
        blank=True
    )

    learning_style = models.CharField(
        max_length=20,
        choices=LEARNING_STYLE_CHOICES,
        default='unsure'
    )

    learning_goals = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username