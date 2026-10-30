from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import UserProfile


@login_required(login_url='/accounts/login/')
def home(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        language = request.POST.get('preferred_language', 'en')

        allowed_languages = ['en', 'hi', 'mr']

        if not username or not email:
            messages.error(request, 'Username and email are required.')

        elif language not in allowed_languages:
            messages.error(request, 'Please select a valid language.')

        elif request.user.__class__.objects.exclude(
            pk=request.user.pk
        ).filter(username=username).exists():
            messages.error(request, 'That username is already taken.')

        elif request.user.__class__.objects.exclude(
            pk=request.user.pk
        ).filter(email=email).exists():
            messages.error(request, 'That email is already in use.')

        else:
            request.user.username = username
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()

            profile.preferred_language = language

            photo = request.FILES.get('profile_photo')

            if photo:
                profile.profile_photo = photo

            profile.save()

            messages.success(request, 'Your settings have been updated.')
            return redirect('user_settings:home')

    context = {
        'page_title': 'User Settings',
        'profile': profile,
    }

    return render(
        request,
        'user_settings/home.html',
        context
    )