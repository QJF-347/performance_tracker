from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    ROLE_CHOICES = (
        ('student', 'student'), 
        ('parent', 'parent'), 
        ('admin', 'admin'), 
        ('teacher', 'teacher'), 
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(max_length=254, unique=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.username} -> {self.role}'