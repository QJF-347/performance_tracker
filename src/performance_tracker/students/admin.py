from django.contrib import admin
from .models import Student, Subject, PerformanceRecord, CourseEnrollment

# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(PerformanceRecord)
admin.site.register(CourseEnrollment)