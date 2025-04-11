from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MediaItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media_images/', blank=True, null=True)
    release_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class UserLibraryItem(models.Model):
    STATUS_CHOICES = [
        ('planned', 'В планах'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('abandoned', 'Брошено'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # ← Было user, стало owner
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    personal_rating = models.PositiveIntegerField(null=True, blank=True)
    started_at = models.DateField(null=True, blank=True)
    finished_at = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('owner', 'media_item')

    def __str__(self):
        return f"{self.owner.username} – {self.media_item.title}"

class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username} - {self.media_item.title}"
