from django.contrib import admin
from .models import (Classroom, Student, Subject, 
                     PerformanceRecord, Event, Message, 
                     AssessmentComponent, ParticipationRecord, 
                     AttendanceRecord, StudentPerformance)

# Register your models here.

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(PerformanceRecord)
admin.site.register(Message)
admin.site.register(AssessmentComponent)
admin.site.register(Event)
admin.site.register(Classroom)
admin.site.register(ParticipationRecord)
admin.site.register(AttendanceRecord)
admin.site.register(StudentPerformance)
