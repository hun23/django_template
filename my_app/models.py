from django.db import models

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    thumbnail = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    