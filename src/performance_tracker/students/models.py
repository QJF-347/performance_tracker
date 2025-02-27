from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    year_of_study = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject, related_name="students")

    def __str__(self):
        return f"{self.user.username} - {self.year_of_study}"

class PerformanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="performance_records")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.FloatField()
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} ({self.score})"


class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
