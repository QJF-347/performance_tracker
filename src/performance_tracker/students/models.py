from django.db import models
from django.contrib.auth import get_user_model

User  = get_user_model()
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE, related_name="student_profile")
    year_of_study = models.CharField(max_length=50) 
    subjects = models.JSONField(default=list)
    performance_data = models.JSONField(default=dict)
    
    def __str__(self):
        return f'{self.user.username} - {self.year_of_study}'