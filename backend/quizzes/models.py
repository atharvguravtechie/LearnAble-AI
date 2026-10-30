from django.db import models
from django.contrib.auth.models import User
from learning.models import Subject, Topic


class Quiz(models.Model):

    QUIZ_TYPE_CHOICES = [
        ('topic', 'Topic Quiz'),
        ('subject', 'Subject Quiz'),
    ]

    title = models.CharField(max_length=200)

    quiz_type = models.CharField(
        max_length=20,
        choices=QUIZ_TYPE_CHOICES
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='quizzes',
        null=True,
        blank=True
    )

    total_questions = models.PositiveIntegerField()

    total_marks = models.PositiveIntegerField()

    duration_minutes = models.PositiveIntegerField(default=30)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D'),
        ]
    )

    explanation = models.TextField(blank=True)

    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.question_text[:80]


class QuizAttempt(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    score = models.PositiveIntegerField(default=0)

    total_marks = models.PositiveIntegerField(default=0)

    correct_answers = models.PositiveIntegerField(default=0)

    wrong_answers = models.PositiveIntegerField(default=0)

    started_at = models.DateTimeField(auto_now_add=True)

    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"


class StudentAnswer(models.Model):

    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='student_answers'
    )

    selected_answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES
    )

    is_correct = models.BooleanField(default=False)

    marks_obtained = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"{self.attempt.student.username} - Answer"