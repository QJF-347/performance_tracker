from django.shortcuts import render
from.models import Student
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import StudentRegisterSerializer, StudentProfileSerializer
from users.models import User

class StudentRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentRegisterSerializer
    permission_classes = [AllowAny,]


class CompleteStudentProfileView(generics.UpdateAPIView):
    serializer_class = StudentProfileSerializer
    queryset = Student.objects.all()

    def get_object(self):
        return self.request.user.student_profile  # Get the student's profile

    def update(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = self.get_serializer(student, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Student profile updated successfully!", "status": "success"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
