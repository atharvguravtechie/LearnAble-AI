
from django.db.models import Sum, Avg, Count, F, ExpressionWrapper, FloatField
from progress.models import StudentTopicProgress, LearningActivity
from quizzes.models import QuizAttempt


def get_student_dashboard_stats(student):
    completed_topics = StudentTopicProgress.objects.filter(
        student=student,
        status='completed'
    ).count()

    total_topics = StudentTopicProgress.objects.filter(
        student=student
    ).count()

    total_study_minutes = LearningActivity.objects.filter(
        student=student
    ).aggregate(
        total=Sum('duration_minutes')
    )['total'] or 0

    quiz_attempts = QuizAttempt.objects.filter(
        student=student,
        total_marks__gt=0
    )

    quiz_stats = quiz_attempts.aggregate(
        total_quizzes=Count('id'),
        average_score=Avg(
            ExpressionWrapper(
                F('score') * 100.0 / F('total_marks'),
                output_field=FloatField()
            )
        )
    )

    return {
        'completed_topics': completed_topics,
        'total_topics_tracked': total_topics,
        'total_study_minutes': total_study_minutes,
        'total_quizzes': quiz_stats['total_quizzes'] or 0,
        'average_quiz_score': round(quiz_stats['average_score'] or 0, 2),
    }
