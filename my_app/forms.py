from django.db import models
from django import forms
from .models import Page

# Create your models here.
class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = "__all__"