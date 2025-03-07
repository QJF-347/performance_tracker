from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate

from rest_framework import generics, status, exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView


from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

    
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            username = data.get("username")
            password = data.get("password")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == "teacher":
                return JsonResponse({"message": "Login successful", "redirect_url": "/pages/teacherdash/"})
            elif user.role == "student": 
                return JsonResponse({"message": "Login successful", "redirect_url": "/pages/studentdash/"})
            elif user.role == "admin":
                return JsonResponse({"message": "Login successful", "redirect_url": "/pages/admindash/"})
            else:
                return JsonResponse({"message": "Login successful", "redirect_url": "/pages/parentdash/"})
                
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def user_logout(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully", "redirect_url": "/pages/login/"})

@csrf_exempt  
def user_register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            password2 = data.get("password2")
            role = data.get("role")

            if password != password2:
                return JsonResponse({"error": "Passwords do not match"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already registered"}, status=400)

            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name
            )
            user.save()

            return JsonResponse({"message": "Registration successful", "redirect_url": "/pages/login/"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = True  
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    