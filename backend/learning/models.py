from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=150)

    education_level = models.CharField(max_length=50)

    class_or_grade = models.CharField(max_length=50)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.class_or_grade}"


class Chapter(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='chapters'
    )

    name = models.CharField(max_length=150)

    chapter_number = models.PositiveIntegerField()

    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.chapter_number}. {self.name}"


class Topic(models.Model):
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='topics'
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    topic_number = models.PositiveIntegerField()

    def __str__(self):
        return self.name