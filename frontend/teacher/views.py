from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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