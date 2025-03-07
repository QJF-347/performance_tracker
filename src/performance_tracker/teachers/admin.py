from django.contrib import admin
from .models import Teacher, TeacherAttendanceRecord, TeacherPerformanceMetrics

admin.site.register(Teacher)
admin.site.register(TeacherPerformanceMetrics)
admin.site.register(TeacherAttendanceRecord)