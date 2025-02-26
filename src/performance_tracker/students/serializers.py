from rest_framework import serializers
from users.serializers import RegisterSerializer
from .models import Student
from users.models import User

class StudentRegisterSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()
    year_of_study = serializers.CharField(max_length=50)
    subjects = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False
    )

    class Meta:
        model = Student
        fields = ['user', 'year_of_study', 'subjects']

    def create(self, validated_data):
        # Extract user data
        user_data = validated_data.pop('user')

        # Extract optional fields
        subjects = validated_data.pop('subjects', [])
        year_of_study = validated_data.pop('year_of_study')

        # Create User using RegisterSerializer
        user_serializer = RegisterSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Create Student linked to the User
        student = Student.objects.create(
            user=user,
            year_of_study=year_of_study,
            subjects=subjects,  # Stored as JSON
            performance_data={}  # Default empty dict
        )

        return student


class StudentProfileSerializer(serializers.ModelSerializer):
    subjects = serializers.ListField(child=serializers.CharField(), required=True)

    class Meta:
        model = Student
        fields = ['year_of_study', 'subjects']
