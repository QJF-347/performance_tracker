from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from students import views

router = routers.DefaultRouter()
router.register(r'subjects', views.SubjectViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'assessment-components', views.AssessmentComponentViewSet)
router.register(r'performance-records', views.PerformanceRecordViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]