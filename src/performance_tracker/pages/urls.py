from django.urls import path
from .views import students_management, subject_page, login_page, register_page, profile_page

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('profile/', profile_page, name='profile'),
    path('subjects/', subject_page, name='subjects'),
    path('students/', students_management, name='students'),
]
