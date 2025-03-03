from rest_framework import viewsets, permissions, response
from .models import Subject, Student, AssessmentComponent, PerformanceRecord, Event, Message
from .serializers import (SubjectSerializer, StudentSerializer, AssessmentComponentSerializer, 
      PerformanceRecordSerializer, EventSerializer, MessageSerializer)
from django.contrib.auth import get_user_model
from .permissions import IsAdminOrTeacher
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacher]
    authentication_classes = [JWTAuthentication]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data)

class AssessmentComponentViewSet(viewsets.ModelViewSet):
    queryset = AssessmentComponent.objects.all()
    serializer_class = AssessmentComponentSerializer

class PerformanceRecordViewSet(viewsets.ModelViewSet):
    queryset = PerformanceRecord.objects.all()
    serializer_class = PerformanceRecordSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
