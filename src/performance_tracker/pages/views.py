from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsStudent, IsTeacher, IsParent

class StudentDashboard(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        return Response({"message": "Welcome Student!"})

class TeacherDashboard(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        return Response({"message": "Welcome Teacher!"})

class ParentDashboard(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def get(self, request):
        return Response({"message": "Welcome Parent!"})

from django.shortcuts import render

def login_page(request):
    return render(request, 'pages/login.html')

def register_page(request):
    return render(request, 'pages/register.html')

def profile_page(request):
    return render(request, 'pages/profile.html')

def subject_page(request):
    return render(request, 'pages/subjects.html')

def students_management(request):
    return render(request, 'pages/students.html')