from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/accounts/login/')
def home(request):
    subjects = [
        'Mathematics',
        'Science',
        'Physics',
        'Chemistry',
        'Biology',
        'Computer Science',
        'English',
        'Other',
    ]

    answer = None
    question = ''
    selected_subject = 'Mathematics'

    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        selected_subject = request.POST.get('subject', 'Mathematics')

        if question:
            answer = (
                "Thank you for asking! This is a demo response. "
                "Gemini AI will be connected later to provide a detailed, "
                "step-by-step explanation for your question."
            )

    context = {
        'page_title': 'Ask a Doubt',
        'subjects': subjects,
        'answer': answer,
        'question': question,
        'selected_subject': selected_subject,
    }

    return render(request, 'doubts/home.html', context)