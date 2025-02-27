from django.urls import path
from .views import (
    SubjectListCreateView, SubjectRetrieveUpdateDestroyView,
    StudentListCreateView, StudentRetrieveUpdateDestroyView,
    PerformanceRecordListCreateView, PerformanceRecordRetrieveUpdateDestroyView,
    CourseEnrollmentListCreateView, CourseEnrollmentRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Subjects
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroyView.as_view(), name='subject-retrieve-update-destroy'),

    # Students
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyView.as_view(), name='student-retrieve-update-destroy'),

    # Performance Records
    path('performance-records/', PerformanceRecordListCreateView.as_view(), name='performance-record-list-create'),
    path('performance-records/<int:pk>/', PerformanceRecordRetrieveUpdateDestroyView.as_view(), name='performance-record-retrieve-update-destroy'),

    # Course Enrollments
    path('course-enrollments/', CourseEnrollmentListCreateView.as_view(), name='course-enrollment-list-create'),
    path('course-enrollments/<int:pk>/', CourseEnrollmentRetrieveUpdateDestroyView.as_view(), name='course-enrollment-retrieve-update-destroy'),
]