from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from  project.settings import EMAIL_HOST_USER

from .models import MediaItem, UserLibraryItem
from .forms import RegisterForm


def index(request):
    media = MediaItem.objects.all()
    return render(request, 'library/index.html', {'media': media})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            subject = 'Добро пожаловать в медиабиблиотеку!'
            message = f'Привет, {user.username}!\n\nСпасибо за регистрацию в нашем сервисе.'
            from_email = EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'library/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'library/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


def my_library(request):
    if not request.user.is_authenticated:
        return redirect('login')

    items = UserLibraryItem.objects.filter(owner=request.user)
    return render(request, 'library/my_library.html', {'items': items})
