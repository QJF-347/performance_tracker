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
        print("--- StudentSerializer update() ---")
        print("Instance:", instance)
        print("Validated Data:", validated_data)

        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()

        instance.year_of_study = validated_data.get('year_of_study', instance.year_of_study)
        instance.subjects.set(validated_data.get('subjects', instance.subjects.all()))

        instance.save()
        print("Updated Instance:", instance)
        print("--- End of update() ---")
        return instance
        
class PerformanceRecordSerializer(serializers.Serializer):
    class Meta:
        model = PerformanceRecord
        fields = ['id', 'student', 'subject', 'score', 'date_recorded']
        
class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = ('id', 'student', 'subject', 'enrollment_date')