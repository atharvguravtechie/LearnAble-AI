from django.db import models
from django.utils.text import slugify


class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='subjects/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='topics'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'title']
        unique_together = ('subject', 'title')

    def __str__(self):
        return f'{self.subject.name} - {self.title}'


class Lesson(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f'{self.topic.title} - {self.title}'