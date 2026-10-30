from django.db import models
from django.contrib.auth.models import User
from learning.models import Topic


class StudentTopicProgress(models.Model):

    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('needs_revision', 'Needs Revision'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='topic_progress'
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='student_progress'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )

    completion_percentage = models.PositiveSmallIntegerField(default=0)

    time_spent_minutes = models.PositiveIntegerField(default=0)

    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'topic')

    def __str__(self):
        return f"{self.student.username} - {self.topic.name}"
class LearningActivity(models.Model):

    ACTIVITY_CHOICES = [
        ('lesson', 'Lesson Studied'),
        ('topic', 'Topic Completed'),
        ('quiz', 'Quiz Attempted'),
        ('revision', 'Revision'),
        ('practice', 'Practice'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='learning_activities'
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='learning_activities'
    )

    description = models.CharField(max_length=255, blank=True)

    duration_minutes = models.PositiveIntegerField(default=0)

    activity_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.activity_type}"