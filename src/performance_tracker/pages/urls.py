from django.urls import path
from .views import (teacher_dash, teacher_detail, admin_dash, 
                    teachers_attendance, classrooms_management, 
                    teachers_management, events_management, 
                    students_management, subject_page, login_page, 
                    register_page, profile_page, classroom_detail, 
                    about_page, contact_page, home_page,parent_dash, 
                    add_performance, student_dash, performance_records, 
                    attendance, participation
                    )

urlpatterns = [
    path('home/', home_page, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('profile/', profile_page, name='profile'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('admindash/', admin_dash, name='admindash'),
    path('studentdash/', student_dash, name='studentdash'),
    path('parentdash/', parent_dash, name='parentdash'),
    path('teacherdash/', teacher_dash, name='teacherdash'),
    path('subjects/', subject_page, name='subjects'),
    path('students/', students_management, name='students'),
    path('events/', events_management, name='events'),
    path('teachers/', teachers_management, name='teachers'),
    path('classrooms/<int:classroom_id>/', classroom_detail, name='classroom_detail'),
    path('classrooms/', classrooms_management, name='classrooms'),
    path('attendances/', teachers_attendance, name='teachers-attendace'),
    path('teachers/<int:teacher_id>/', teacher_detail, name='teacher_detail'),
    path('addperformance/', add_performance, name='add-performance'),
    path('performancerecords/<int:student_id>/', performance_records, name='performancerecords'),
    path('attendance/<int:student_id>/', attendance, name='attendance'),
    path('participation/<int:student_id>/', participation, name='participation'),
]
