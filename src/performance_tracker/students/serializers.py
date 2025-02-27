from rest_framework import serializers
from users.serializers import RegisterSerializer
from .models import Student, Subject, PerformanceRecord, CourseEnrollment
from users.models import User

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class StudentSerializer(serializers.Serializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'year_of_study', 'subjects']

class PerformanceRecordSerializer(serializers.Serializer):
    class Meta:
        model = PerformanceRecord
        fields = ['id', 'student', 'subject', 'score', 'date_recorded']