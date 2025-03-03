from rest_framework import serializers
from .models import Subject, Student, AssessmentComponent, PerformanceRecord, Event, Message
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

User = get_user_model()

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Read-only nested serializer
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )  # Write-only pk field
    subjects = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Student
        fields = ('id', 'user', 'user_id', 'year_of_study', 'subjects', 'parent')

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        subjects_data = validated_data.pop('subjects') # Get the subjects data
        validated_data['user'] = user_id
        student = Student.objects.create(**validated_data)
        student.subjects.set(subjects_data) # Use .set() to assign subjects
        return student

    def update(self, instance, validated_data):
        user_id = validated_data.pop('user_id', None)
        if user_id is not None:
            instance.user = user_id
        instance.year_of_study = validated_data.get('year_of_study', instance.year_of_study)
        instance.subjects.set(validated_data.get('subjects', instance.subjects.all()))
        instance.parent = validated_data.get('parent', instance.parent)
        instance.save()
        return instance

class AssessmentComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentComponent
        fields = '__all__'

class PerformanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceRecord
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
