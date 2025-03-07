from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet, TeacherAttendanceRecordListCreateView, TeacherAttendanceRecordRetrieveUpdateDestroyView, TeacherAttendanceRecordFilterByDateView
from django.urls import path, include

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet, basename='teacher')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/attendance/', TeacherAttendanceRecordListCreateView.as_view(), name='attendance-list-create'),
    path('api/attendance/<int:pk>/', TeacherAttendanceRecordRetrieveUpdateDestroyView.as_view(), name='attendance-retrieve-update-destroy'),
    path('api/attendance/date/', TeacherAttendanceRecordFilterByDateView.as_view(), name='attendance-filter-date'),
]