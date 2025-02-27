from django.shortcuts import render
from.models import Student, Subject, PerformanceRecord
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SubjectSerializer, StudentSerializer, PerformanceRecordSerializer
from users.models import User
from django.shortcuts import get_object_or_404

class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    
class StudentProfileView(generics.RetrieveAPIView):
    serializer_class =StudentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(Student, user=self.request.user)