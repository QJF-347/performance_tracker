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
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="children") # Added parent field.

    def __str__(self):
        return f"{self.user.username} - {self.year_of_study}"

class AssessmentComponent(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class PerformanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="performance_records")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assessment_component = models.ForeignKey(AssessmentComponent, on_delete=models.CASCADE)
    score = models.FloatField()
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} - {self.assessment_component.name} ({self.score})"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.title } :> {self.date}'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"