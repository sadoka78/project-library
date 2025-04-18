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
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MediaItemForm, UserLibraryItemForm

@login_required
def add_new_media_to_library(request):
    if request.method == 'POST':
        media_form = MediaItemForm(request.POST, request.FILES)
        library_form = UserLibraryItemForm(request.POST)

        if media_form.is_valid() and library_form.is_valid():
            media_item = media_form.save()

            library_item = library_form.save(commit=False)
            library_item.media_item = media_item
            library_item.owner = request.user
            library_item.save()

            return redirect('my_library')
    else:
        media_form = MediaItemForm()
        library_form = UserLibraryItemForm()

    return render(request, 'library/add_new_to_library.html', {
        'media_form': media_form,
        'library_form': library_form,
    })


from .forms import CategoryForm


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_new_media_to_library')  # Назад к добавлению медиа
    else:
        form = CategoryForm()

    return render(request, 'library/create_category.html', {'form': form})

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserLibraryItem
from .forms import UserLibraryItemForm

@login_required
def edit_library_item(request, pk):
    item = get_object_or_404(UserLibraryItem, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = UserLibraryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('my_library')
    else:
        form = UserLibraryItemForm(instance=item)

    return render(request, 'library/edit_library_item.html', {'form': form, 'item': item})


@login_required
def delete_library_item(request, pk):
    item = get_object_or_404(UserLibraryItem, pk=pk, owner=request.user)

    if request.method == 'POST':
        item.delete()
        return redirect('my_library')

    return render(request, 'library/delete_library_item.html', {'item': item})
