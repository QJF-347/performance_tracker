from rest_framework import serializers
from users.serializers import RegisterSerializer
from .models import Student, Subject, PerformanceRecord, CourseEnrollment
from users.models import User
from users.serializers import UserSerializer

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subjects = serializers.PrimaryKeyRelatedField(many=True, queryset=Subject.objects.all())

    class Meta:
        model = Student
        fields = ('id', 'user', 'year_of_study', 'subjects')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()
            
        instance.year_of_study = validated_data.get('year_of_study', instance.year_of_study)
        instance.subjects.set(validated_data.get('subjects', instance.subjects.all()))

        instance.save()
        return instance
        
class PerformanceRecordSerializer(serializers.Serializer):
    class Meta:
        model = PerformanceRecord
        fields = ['id', 'student', 'subject', 'score', 'date_recorded']
        
class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = ('id', 'student', 'subject', 'enrollment_date')