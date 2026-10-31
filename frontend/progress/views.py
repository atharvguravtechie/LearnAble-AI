
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from .models import ProgressRecord


@login_required(login_url='/accounts/login/')
def home(request):

    records = ProgressRecord.objects.filter(
        user=request.user
    ).order_by('-completed_at')

    total_activities = records.count()

    # Quiz records with valid total marks
    quiz_records = records.filter(
        activity_type='quiz',
        total__gt=0
    )

    # Calculate average quiz percentage using combined marks
    quiz_totals = quiz_records.aggregate(
        total_score=Sum('score'),
        total_marks=Sum('total')
    )

    total_score = quiz_totals['total_score'] or 0
    total_marks = quiz_totals['total_marks'] or 0

    if total_marks > 0:
        quiz_percentage = round(
            (total_score / total_marks) * 100
        )
    else:
        quiz_percentage = 0

    context = {
        'page_title': 'Progress Tracker',
        'records': records[:20],

        'total_activities': total_activities,
        'average_score': quiz_percentage,
        'quiz_percentage': quiz_percentage,

        'lesson_count': records.filter(
            activity_type='lesson'
        ).count(),

        'quiz_count': quiz_records.count(),

        'notes_count': records.filter(
            activity_type='notes'
        ).count(),
    }

    return render(
        request,
        'progress/home.html',
        context
    )
