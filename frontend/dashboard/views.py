
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum

from learning.models import Subject
from progress.models import ProgressRecord


@login_required(login_url='/accounts/login/')
def home(request):

    user = request.user
    today = timezone.localdate()

    # Student information
    student_name = user.first_name if user.first_name else user.username

    # Total subjects available in the learning system
    total_subjects = Subject.objects.count()

    # Get this student's progress records
    progress_records = ProgressRecord.objects.filter(user=user)

    # Total completed lessons recorded for this student
    lessons_completed = progress_records.filter(
        activity_type='lesson'
    ).count()

    # Calculate average quiz percentage using total marks
    quiz_records = progress_records.filter(
        activity_type='quiz'
    )

    quiz_totals = quiz_records.aggregate(
        total_score=Sum('score'),
        total_marks=Sum('total')
    )

    total_score = quiz_totals['total_score'] or 0
    total_marks = quiz_totals['total_marks'] or 0

    if total_marks > 0:
        average_score = round(
            (total_score / total_marks) * 100
        )
    else:
        average_score = 0

    # Calculate learning streak
    activity_dates = set(
        progress_records.values_list(
            'completed_at__date',
            flat=True
        ).distinct()
    )

    if today in activity_dates:
        current_date = today
    elif (today - timezone.timedelta(days=1)) in activity_dates:
        current_date = today - timezone.timedelta(days=1)
    else:
        current_date = None

    learning_streak = 0

    while current_date and current_date in activity_dates:
        learning_streak += 1
        current_date -= timezone.timedelta(days=1)

    # Get the five most recent activities
    recent_records = progress_records.order_by(
        '-completed_at'
    )[:5]

    recent_activities = []

    for record in recent_records:

        activity_name = record.get_activity_type_display()

        if record.activity_type == 'quiz' and record.total > 0:
            description = (
                f"Completed {activity_name} - "
                f"{record.score}/{record.total} marks "
                f"({record.percentage}%)"
            )

        else:
            description = (
                f"Completed {activity_name} activity"
            )

        recent_activities.append({
            'title': record.title,
            'description': description,
        })

    context = {
        'student_name': student_name,
        'student_email': user.email,
        'today': today,

        'total_subjects': total_subjects,
        'lessons_completed': lessons_completed,
        'average_score': average_score,
        'learning_streak': learning_streak,

        'recent_activities': recent_activities,
    }

    return render(
        request,
        'dashboard/home.html',
        context
    )
