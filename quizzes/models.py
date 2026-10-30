
from django.db import models


class Question(models.Model):
    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    question_text = models.TextField()

    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)

    CORRECT_OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    correct_option = models.CharField(
        max_length=1,
        choices=CORRECT_OPTION_CHOICES
    )

    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['subject', 'topic']

    def __str__(self):
        return f"{self.subject} - {self.topic}: {self.question_text[:60]}"
