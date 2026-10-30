from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('learning/', include('learning.urls')),
    path('teacher/', include('teacher.urls')),
    path('doubts/', include('doubts.urls')),
    path('notes/', include('notes.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('progress/', include('progress.urls')),
    path('settings/', include('user_settings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )