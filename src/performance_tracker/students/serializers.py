from rest_framework import serializers
from .models import Subject, Student, AssessmentComponent, PerformanceRecord, Event, Message, AttendanceRecord, ParticipationRecord, StudentPerformance
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
from django.apps import apps

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
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    component_name = serializers.CharField(source="assessment_component.name", read_only=True)

    class Meta:
        model = PerformanceRecord
        fields = ['id', 'score', 'date_recorded', 'student', 'subject', 'assessment_component', 'subject_name', 'component_name']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date', 'location')
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'date': {'required': False},
            'location': {'required': False},
        }

    def update(self, instance, validated_data):
        # Update only the fields that are present in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ClassroomSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=apps.get_model("teachers", "Teacher").objects.all()
    )
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=apps.get_model("students", "Student").objects.all(),
        required=False
    )
    subjects = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Subject.objects.all(),
        required=False
    )

    class Meta:
        model = apps.get_model("students", "Classroom") #Using string representation for model
        fields = ('id', 'name', 'teachers', 'students', 'subjects', 'description')

class AttendanceRecordSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source="classroom.name", read_only=True)
    class Meta:
        model = AttendanceRecord
        fields = ["student", "id", "classroom", "date", "present", "classroom_name"]
        
class ParticipationRecordSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source="classroom.name", read_only=True)
    class Meta:
        model = ParticipationRecord
        fields = ["id", "classroom_name", "student", "date", "score"]
        
class StudentPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPerformance
        fields = "__all__"
        
        