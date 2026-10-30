from django.contrib import admin
from .models import ProgressRecord


@admin.register(ProgressRecord)
class ProgressRecordAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'activity_type',
        'title',
        'score',
        'total',
        'completed_at',
    )

    list_filter = (
        'activity_type',
        'completed_at',
    )

    search_fields = (
        'user__username',
        'title',
    )