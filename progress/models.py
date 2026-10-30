from django.db import models
from django.contrib.auth.models import User


class ProgressRecord(models.Model):

    ACTIVITY_CHOICES = [
        ('lesson', 'Lesson'),
        ('quiz', 'Quiz'),
        ('notes', 'Notes'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES
    )

    title = models.CharField(max_length=200)

    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    @property
    def percentage(self):
        if self.total > 0:
            return round((self.score / self.total) * 100)
        return 0