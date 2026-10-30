
from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question_text',
        'subject',
        'topic',
        'correct_option',
        'created_at',
    )

    list_filter = ('subject', 'topic')
    search_fields = ('question_text', 'subject', 'topic')
