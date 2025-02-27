from django.urls import path
from .views import SubjectListView, StudentProfileView

urlpatterns = [
    path('subjects/', SubjectListView.as_view(), name='subjects'),
    path('profile/', StudentProfileView.as_view(), name='student-profile'),
]
