from django.contrib import admin
from .models import Student, Subject, PerformanceRecord, Event, Message, AssessmentComponent

# Register your models here.

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(PerformanceRecord)
admin.site.register(Message)
admin.site.register(AssessmentComponent)
admin.site.register(Event)
