from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, MediaItem, UserLibraryItem, Review

admin.site.register(Category)
admin.site.register(MediaItem)
admin.site.register(UserLibraryItem)
admin.site.register(Review)
