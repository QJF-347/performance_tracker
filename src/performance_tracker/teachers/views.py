from rest_framework import viewsets, permissions, generics, filters
from .models import Teacher , TeacherAttendanceRecord
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import TeacherSerializer, TeacherAttendanceRecordSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
import django_filters


User = get_user_model()

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeacherAttendanceRecordFilter(django_filters.FilterSet):
    teacher_name = django_filters.CharFilter(field_name='teacher__user__get_full_name', lookup_expr='icontains')
    classroom_name = django_filters.CharFilter(field_name='classroom__name', lookup_expr='icontains')
    date = django_filters.DateFilter(field_name='date')
    present = django_filters.BooleanFilter(field_name='present')

    class Meta:
        model = TeacherAttendanceRecord
        fields = ['teacher_name', 'classroom_name', 'date', 'present']

class TeacherAttendanceRecordListView(generics.ListAPIView):
    queryset = TeacherAttendanceRecord.objects.all()
    serializer_class = TeacherAttendanceRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TeacherAttendanceRecordFilter

class TeacherAttendanceRecordListCreateView(generics.ListCreateAPIView):
    queryset = TeacherAttendanceRecord.objects.all()
    serializer_class = TeacherAttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

class TeacherAttendanceRecordRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeacherAttendanceRecord.objects.all()
    serializer_class = TeacherAttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

class TeacherAttendanceRecordFilterByDateView(generics.ListAPIView):
    serializer_class = TeacherAttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        date_str = self.request.query_params.get('date', None)
        if date_str:
            return TeacherAttendanceRecord.objects.filter(date=date_str)
        else:
            return TeacherAttendanceRecord.objects.all()