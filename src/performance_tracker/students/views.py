from django.shortcuts import render
from.models import Student, Subject, PerformanceRecord, CourseEnrollment
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import SubjectSerializer, StudentSerializer, PerformanceRecordSerializer, CourseEnrollmentSerializer
from .permissions import IsAdminOrTeacher
from django.shortcuts import get_object_or_404
from users.models import User

# subject views
class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher, ]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class SubjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

# student views
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    
class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'year_of_study']
    ordering_fields = ['user__username', 'year_of_study']
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


# Performance Record Views
class PerformanceRecordListCreateView(generics.ListCreateAPIView):
    queryset = PerformanceRecord.objects.all()
    serializer_class = PerformanceRecordSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]


class PerformanceRecordRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PerformanceRecord.objects.all()
    serializer_class = PerformanceRecordSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]


# Course Enrollment Views
class CourseEnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]


class CourseEnrollmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]