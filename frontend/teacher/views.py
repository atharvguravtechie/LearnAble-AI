
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from progress.models import ProgressRecord


@login_required(login_url='/accounts/login/')
def home(request):
    context = {
        'page_title': 'AI Teacher',
        'languages': [
            {'code': 'en-US', 'name': 'English'},
            {'code': 'hi-IN', 'name': 'Hindi'},
            {'code': 'mr-IN', 'name': 'Marathi'},
        ],
    }

    return render(request, 'teacher/home.html', context)


@login_required(login_url='/accounts/login/')
@require_POST
def record_activity(request):
    import json

    try:
        data = json.loads(request.body)
        question = str(data.get('question', '')).strip()

        if not question:
            return JsonResponse({
                'success': False,
                'error': 'Question is required.'
            }, status=400)

        ProgressRecord.objects.create(
            user=request.user,
            activity_type='lesson',
            title=f'AI Teacher: {question[:150]}',
            score=0,
            total=0,
        )

        return JsonResponse({'success': True})

    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse({
            'success': False,
            'error': 'Invalid request.'
        }, status=400)
