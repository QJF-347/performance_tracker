from rest_framework import viewsets, permissions, response
from .models import Subject, Student, AssessmentComponent, PerformanceRecord, Event, Message, Classroom, AttendanceRecord, ParticipationRecord, StudentPerformance
from .serializers import (SubjectSerializer, StudentSerializer, AssessmentComponentSerializer, AttendanceRecordSerializer, 
      PerformanceRecordSerializer, EventSerializer, MessageSerializer, ClassroomSerializer, ParticipationRecordSerializer, StudentPerformanceSerializer)
from django.contrib.auth import get_user_model
from .permissions import IsAdminOrTeacher
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, mixins


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
    permission_classes = [IsAdminOrTeacher]

class PerformanceRecordViewSet(viewsets.ModelViewSet):
    queryset = PerformanceRecord.objects.all()
    serializer_class = PerformanceRecordSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    
class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.student.performance_summary.update_student_performance(instance.student)
    
    
class ParticipationRecordViewSet(viewsets.ModelViewSet):
    queryset = ParticipationRecord.objects.all()
    serializer_class = ParticipationRecordSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.student.performance_summary.update_student_performance(instance.student)

class StudentPerformanceViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = StudentPerformance.objects.all()
    serializer_class = StudentPerformanceSerializer
    lookup_field = "student__id"