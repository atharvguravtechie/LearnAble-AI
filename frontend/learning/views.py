
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Subject, Topic, Lesson
from progress.models import ProgressRecord


@login_required(login_url='/accounts/login/')
def subject_list(request):

    subjects = Subject.objects.all()

    return render(
        request,
        'learning/subjects.html',
        {'subjects': subjects}
    )


@login_required(login_url='/accounts/login/')
def topic_list(request, subject_id):

    subject = get_object_or_404(Subject, id=subject_id)
    topics = subject.topics.all()

    return render(
        request,
        'learning/topics.html',
        {
            'subject': subject,
            'topics': topics,
        }
    )


@login_required(login_url='/accounts/login/')
def lesson_detail(request, lesson_id):

    lesson = get_object_or_404(
        Lesson.objects.select_related('topic__subject'),
        id=lesson_id
    )

    activity_title = f'Lesson ID: {lesson.id}'

    completed = ProgressRecord.objects.filter(
        user=request.user,
        activity_type='lesson',
        title=activity_title
    ).exists()

    if request.method == 'POST':

        if not completed:

            ProgressRecord.objects.create(
                user=request.user,
                activity_type='lesson',
                title=activity_title,
                score=0,
                total=0,
            )

            messages.success(
                request,
                'Lesson marked as completed! Your progress has been updated.'
            )

        else:

            messages.info(
                request,
                'You have already completed this lesson.'
            )

        return redirect(
            'learning:lesson_detail',
            lesson_id=lesson.id
        )

    return render(
        request,
        'learning/lesson_detail.html',
        {
            'lesson': lesson,
            'completed': completed,
        }
    )
