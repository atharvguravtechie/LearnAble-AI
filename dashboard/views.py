from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def home(request):

    context = {
        'total_subjects': 0,
        'lessons_completed': 0,
        'average_score': 0,
        'learning_streak': 0,
        'recent_activities': [],
    }

    return render(
        request,
        'dashboard/home.html',
        context
    )