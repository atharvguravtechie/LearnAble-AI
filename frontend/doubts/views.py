
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

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
    error = None

    if request.method == 'POST':

        question = request.POST.get('question', '').strip()
        selected_subject = request.POST.get('subject', 'Mathematics')

        if selected_subject not in subjects:
            selected_subject = 'Other'

        if not question:
            error = 'Please enter your question.'

        else:
            # Include the selected subject in the AI question.
            full_question = (
                f"Subject: {selected_subject}\n"
                f"Student's question: {question}\n\n"
                "Explain this question step by step in simple language."
            )

            payload = {
                'question': full_question,
                'language': 'English',
            }

            try:
                api_request = Request(
                    'http://127.0.0.1:8001/api/teacher/ask/',
                    data=json.dumps(payload).encode('utf-8'),
                    headers={
                        'Content-Type': 'application/json',
                    },
                    method='POST',
                )

                with urlopen(api_request, timeout=60) as response:
                    result = json.loads(response.read().decode('utf-8'))

                if result.get('success'):
                    answer = result.get('answer')
                else:
                    error = result.get(
                        'error',
                        'Unable to generate an answer.'
                    )

            except HTTPError as e:
                try:
                    error_data = json.loads(e.read().decode('utf-8'))
                    error = error_data.get(
                        'error',
                        'The AI service returned an error.'
                    )
                except Exception:
                    error = 'The AI service returned an error.'

            except URLError:
                error = (
                    'Cannot connect to the AI server. '
                    'Please make sure the backend is running on port 8001.'
                )

            except Exception as e:
                print('Doubt Solver error:', str(e))
                error = 'Something went wrong. Please try again.'

    context = {
        'page_title': 'Ask a Doubt',
        'subjects': subjects,
        'answer': answer,
        'question': question,
        'selected_subject': selected_subject,
        'error': error,
    }

    return render(request, 'doubts/home.html', context)
