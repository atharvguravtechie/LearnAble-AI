from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.shortcuts import render

from .models import ProgressRecord


@login_required(login_url='/accounts/login/')
def home(request):

    records = ProgressRecord.objects.filter(
        user=request.user
    )

    total_activities = records.count()

    quiz_records = records.filter(
        activity_type='quiz',
        total__gt=0
    )

    average_score = quiz_records.aggregate(
        average=Avg('score')
    )['average'] or 0

    total_score = quiz_records.aggregate(
        score=Sum('score'),
        total=Sum('total')
    )

    quiz_percentage = 0

    if total_score['total']:
        quiz_percentage = round(
            (total_score['score'] / total_score['total']) * 100
        )

    context = {
        'page_title': 'Progress Tracker',
        'records': records[:20],
        'total_activities': total_activities,
        'average_score': round(average_score),
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