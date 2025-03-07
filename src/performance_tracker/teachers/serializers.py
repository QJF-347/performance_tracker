from rest_framework import serializers
from .models import Teacher, ClassPerformanceMetrics, TeacherAttendanceRecord
from students.models import Classroom, Subject, Student
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    subjects_taught = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), many=True
    )

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'user_id', 'department', 'subjects_taught')

    def create(self, validated_data):
        print("Creating teacher with validated data:", validated_data)  # Debugging
        try:
            user_id = validated_data.pop('user_id')
            subjects_taught_data = validated_data.pop('subjects_taught')
            validated_data['user'] = user_id
            teacher = Teacher.objects.create(**validated_data)
            teacher.subjects_taught.set(subjects_taught_data)
            return teacher
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "User does not exist."})
        except Subject.DoesNotExist:
            raise serializers.ValidationError({"subjects_taught": "One or more subjects do not exist."})
        except Exception as e:
            print(f"Error creating teacher: {e}")
            raise serializers.ValidationError({"detail": "Error creating teacher."})

    def update(self, instance, validated_data):
        print("Updating teacher with validated data:", validated_data)  # Debugging
        user_id = validated_data.pop('user_id', None)
        if user_id is not None:
            instance.user = user_id
        instance.department = validated_data.get('department', instance.department)
        subjects_taught = validated_data.get('subjects_taught', instance.subjects_taught.all())
        instance.subjects_taught.set(subjects_taught)
        instance.save()
        return instance
 
 
class TeacherAttendanceRecordSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)

    class Meta:
        model = TeacherAttendanceRecord
        fields = ['id', 'teacher', 'teacher_name', 'classroom', 'classroom_name', 'date', 'present']
        read_only_fields = ['date', 'teacher_name', 'classroom_name']

    def create(self, validated_data):
        return TeacherAttendanceRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.teacher = validated_data.get('teacher', instance.teacher)
        instance.classroom = validated_data.get('classroom', instance.classroom)
        instance.present = validated_data.get('present', instance.present)
        instance.save()
        return instance
    
 
class ClassMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassPerformanceMetrics
        fields = ('id', 'average_attendance', 'average_performance', 'average_participation')

