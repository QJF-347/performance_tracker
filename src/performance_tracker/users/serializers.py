from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2', 'role']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove the duplicate password field
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',  'first_name', 'last_name', 'username']

    def validate_username(self, value):
        """Ensure username is unique except for the current user."""
        request = self.context.get("request")
        user_id = self.instance.id if self.instance else None

        if User.objects.filter(username=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        """Ensure email is unique except for the current user."""
        request = self.context.get("request")
        user_id = self.instance.id if self.instance else None

        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value





