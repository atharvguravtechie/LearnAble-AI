import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Question
from progress.models import ProgressRecord


SUBJECTS = [
    'Mathematics',
    'Science',
    'Physics',
    'Chemistry',
    'Biology',
    'Computer Science',
    'English',
    'Other',
]


@login_required(login_url='/accounts/login/')
def home(request):
    context = {
        'page_title': 'Quizzes',
        'subjects': SUBJECTS,
    }

    if request.method == 'POST':
        subject = request.POST.get('subject', 'Other')
        topic = request.POST.get('topic', '').strip()
        quiz_type = request.POST.get('quiz_type', 'topic')

        if subject not in SUBJECTS:
            subject = 'Other'

        if quiz_type not in ['topic', 'subject']:
            quiz_type = 'topic'

        question_count = 30 if quiz_type == 'topic' else 60

        questions = Question.objects.filter(subject=subject)

        if quiz_type == 'topic':
            questions = questions.filter(topic__iexact=topic)

        available_count = questions.count()

        if available_count < question_count:
            context.update({
                'error': (
                    f'This quiz requires {question_count} questions, '
                    f'but only {available_count} are available. '
                    'Please add more questions through Django Admin.'
                ),
                'selected_subject': subject,
                'selected_topic': topic,
                'selected_quiz_type': quiz_type,
            })

            return render(request, 'quizzes/home.html', context)

        question_list = list(questions)
        random.shuffle(question_list)

        selected_questions = question_list[:question_count]

        request.session['quiz_questions'] = [
            question.id for question in selected_questions
        ]

        request.session['quiz_subject'] = subject
        request.session['quiz_topic'] = topic
        request.session['quiz_type'] = quiz_type

        return redirect('quizzes:take_quiz')

    return render(request, 'quizzes/home.html', context)


@login_required(login_url='/accounts/login/')
def take_quiz(request):

    question_ids = request.session.get('quiz_questions')

    if not question_ids:
        return redirect('quizzes:home')

    questions = Question.objects.filter(id__in=question_ids)
    question_map = {
        question.id: question for question in questions
    }

    ordered_questions = [
        question_map[question_id]
        for question_id in question_ids
        if question_id in question_map
    ]

    if len(ordered_questions) != len(question_ids):
        request.session.pop('quiz_questions', None)
        return redirect('quizzes:home')

    if request.method == 'POST':

        score = 0
        results = []

        for question in ordered_questions:

            submitted_answer = request.POST.get(
                f'question_{question.id}',
                ''
            ).upper()

            is_correct = (
                submitted_answer == question.correct_option
            )

            if is_correct:
                score += 1

            results.append({
                'question': question,
                'submitted_answer': submitted_answer,
                'is_correct': is_correct,
            })

        total = len(ordered_questions)

        percentage = (
            round((score / total) * 100, 2)
            if total else 0
        )

        subject = request.session.get(
            'quiz_subject',
            'General'
        )

        topic = request.session.get(
            'quiz_topic',
            ''
        )

        quiz_type = request.session.get(
            'quiz_type',
            'topic'
        )

        if quiz_type == 'subject':
            activity_title = f'{subject} Subject Quiz'
        else:
            activity_title = f'{subject} - {topic} Quiz'

        # Automatically save quiz progress.
        ProgressRecord.objects.create(
            user=request.user,
            activity_type='quiz',
            title=activity_title,
            score=score,
            total=total,
        )

        # Clear the quiz session after saving the result.
        request.session.pop('quiz_questions', None)
        request.session.pop('quiz_subject', None)
        request.session.pop('quiz_topic', None)
        request.session.pop('quiz_type', None)

        return render(request, 'quizzes/result.html', {
            'page_title': 'Quiz Results',
            'results': results,
            'score': score,
            'total': total,
            'percentage': percentage,
        })

    return render(request, 'quizzes/take_quiz.html', {
        'page_title': 'Take Quiz',
        'questions': ordered_questions,
        'total': len(ordered_questions),
        'subject': request.session.get('quiz_subject', ''),
        'topic': request.session.get('quiz_topic', ''),
    })