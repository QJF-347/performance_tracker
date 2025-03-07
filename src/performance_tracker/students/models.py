from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    year_of_study = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject, related_name="students")
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="children")

    def __str__(self):
        return f"{self.user.username} - {self.year_of_study}"

class AssessmentComponent(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class PerformanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="performance_records")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assessment_component = models.ForeignKey(AssessmentComponent, on_delete=models.CASCADE, related_name="performance_records")
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.subject.name} - {self.assessment_component.name} ({self.score})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        StudentPerformance.update_student_performance(self.student)

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.title} :> {self.date}'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField("teachers.Teacher", related_name='classrooms')
    students = models.ManyToManyField("students.Student", related_name='classrooms', blank=True)
    subjects = models.ManyToManyField("students.Subject", related_name="classrooms", blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.classroom.name} - {'Present' if self.present else 'Absent'}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        StudentPerformance.update_student_performance(self.student)

class ParticipationRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="participation_records")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="participation_records")
    date = models.DateField(auto_now_add=True)
    score = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.student.user.username} - {self.classroom.name} - {self.score}/5"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        StudentPerformance.update_student_performance(self.student)

class StudentPerformance(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="performance_summary")
    average_score = models.FloatField(default=0.0)
    attendance_percentage = models.FloatField(default=0.0)
    participation_score = models.FloatField(default=0.0)
    predicted_final_exam = models.FloatField(default=0.0)  # Add this field
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} Performance Summary"

    @staticmethod
    def update_student_performance(student):
        student_performance, _ = StudentPerformance.objects.get_or_create(student=student)

        performance_records = PerformanceRecord.objects.filter(student=student)
        attendance_records = AttendanceRecord.objects.filter(student=student)
        participation_records = ParticipationRecord.objects.filter(student=student)

        student_performance.average_score = performance_records.aggregate(models.Avg("score"))["score__avg"] or 0.0
        total_classes = attendance_records.count()
        attended_classes = attendance_records.filter(present=True).count()
        student_performance.attendance_percentage = (attended_classes / total_classes) * 100 if total_classes > 0 else 0.0
        student_performance.participation_score = participation_records.aggregate(models.Avg("score"))["score__avg"] or 0.0

        student_performance.save()
