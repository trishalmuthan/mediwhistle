from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_site_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Document(models.Model):
    upload = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)

class Form(models.Model):
    subject = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    doctor = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    practice = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='form_files/', null=True, blank=True)  # Optional
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forms', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

# Model for Comments
class Comment(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.form.subject}"
