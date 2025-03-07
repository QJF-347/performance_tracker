from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg
from students.models import Student, Subject, AttendanceRecord, ParticipationRecord, PerformanceRecord


User = get_user_model()

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    department = models.CharField(max_length=100, blank=True, null=True)
    subjects_taught = models.ManyToManyField(Subject, related_name='teachers')

    def __str__(self):
        return self.user.username
    
    def update_performance_metrics(self):
        """Update teacher's performance metrics based on students' performance, attendance, and participation."""
        classes = self.classrooms.all()
        students = Student.objects.filter(classrooms__in=classes).distinct()

        total_attendance_records = AttendanceRecord.objects.filter(student__in=students)
        total_attended = total_attendance_records.filter(present=True).count()
        total_classes = total_attendance_records.count()

        avg_attendance = (total_attended / total_classes * 100) if total_classes else 0  # Avoid division by zero

        avg_participation = ParticipationRecord.objects.filter(
            student__in=students
        ).aggregate(avg_score=Avg('score'))['avg_score'] or 0  # Default to 0 if no records exist

        avg_performance = PerformanceRecord.objects.filter(
            student__in=students
        ).aggregate(avg_score=Avg('score'))['avg_score'] or 0  # Default to 0 if no records exist

        # Update or create teacher performance metrics
        metrics, created = TeacherPerformanceMetrics.objects.get_or_create(teacher=self)
        metrics.average_attendance = avg_attendance
        metrics.average_student_participation = avg_participation
        metrics.average_student_performance = avg_performance
        metrics.save()



class TeacherAttendanceRecord(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="teacher_attendance_records")
    classroom = models.ForeignKey("students.Classroom", on_delete=models.CASCADE, related_name="teacher_attendance")
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.teacher.user.username} - {self.classroom.name} - {'Present' if self.present else 'Absent'}"


class ClassPerformanceMetrics(models.Model):
    classroom = models.OneToOneField("students.Classroom", on_delete=models.CASCADE, related_name="performance_metrics")
    average_attendance = models.FloatField(null=True, blank=True)
    average_performance = models.FloatField(null=True, blank=True)
    average_participation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Metrics for {self.classroom.name}: Attendance={self.average_attendance}, Performance={self.average_performance}, Participation={self.average_participation}"

    def update_metrics(self):
        """Update the class performance metrics dynamically."""
        students = self.classroom.students.all()

        total_attendance = AttendanceRecord.objects.filter(
            student__in=self.classroom.students.all(), present=True
        ).count()
        total_classes = AttendanceRecord.objects.filter(
            student__in=self.classroom.students.all()
        ).count()

        self.average_attendance = (total_attendance / total_classes * 100) if total_classes else 0

        self.average_participation = ParticipationRecord.objects.filter(
            classroom=self.classroom
        ).aggregate(Avg('score'))['score__avg'] or 0

        self.average_performance = PerformanceRecord.objects.filter(
            student__in=students
        ).aggregate(Avg('score'))['score__avg'] or 0

        self.save()

class TeacherPerformanceMetrics(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name="performance_metrics")
    average_attendance = models.FloatField(null=True, blank=True)  # Teacher's attendance rate
    average_student_performance = models.FloatField(null=True, blank=True)  # How well students perform in their classes
    average_student_participation = models.FloatField(null=True, blank=True)  # Student engagement in class

    def __str__(self):
        return f"Teacher {self.teacher.user.username} - Attendance: {self.average_attendance}%, Performance: {self.average_student_performance}, Participation: {self.average_student_participation}"
