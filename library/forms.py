from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MediaItem, UserLibraryItem

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = '__all__'

class UserLibraryItemForm(forms.ModelForm):
    class Meta:
        model = UserLibraryItem
        exclude = ['owner', 'media_item']

from .models import Category
from django import forms

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Название категории'}
