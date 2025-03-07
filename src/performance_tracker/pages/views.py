from students.models import Student, Classroom, Subject, AssessmentComponent, PerformanceRecord
from django.shortcuts import render, get_object_or_404
from teachers.models import Teacher
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from students.models import User, Event, Classroom, AttendanceRecord, ParticipationRecord


def home_page(request):
    return render(request, 'pages/home.html')

def login_page(request):
    return render(request, 'pages/login.html')

def register_page(request):
    return render(request, 'pages/register.html')

def profile_page(request):
    return render(request, 'pages/profile.html')

def about_page(request):
    return render(request, 'pages/about.html')

def contact_page(request):
    return render(request, 'pages/contact.html')

def subject_page(request):
    return render(request, 'pages/subjects.html')

def students_management(request):
    return render(request, 'pages/students.html')

def teachers_management(request):
    return render(request, 'pages/teachers_management.html')

def events_management(request):
    return render(request, 'pages/events.html')

def classrooms_management(request):
    return render(request, 'pages/classroom_management.html')

@login_required
def student_dash(request):
    user = request.user
    student = Student.objects.get(user=user)
    subjects = Subject.objects.all()
    parents = User.objects.filter(role="parent")
    event = Event.objects.all()
    student_subjects = student.subjects.all()
    context = {
        "student":student, 
        "subjects":subjects, 
        "parents":parents, 
        "events":event, 
        "student_subjects":student_subjects, 
    }
    
    return render(request, 'pages/studentdash.html', context)


@login_required
def parent_dash(request):
    parent = request.user 
    children = Student.objects.filter(parent=parent)  

    return render(request, 'pages/parentdash.html', {'children': children})

@login_required
def classroom_detail(request, classroom_id):
    classroom = Classroom.objects.filter(id=classroom_id)

    context = {
        'classroom': classroom
    }
    return render(request, 'pages/classroom_detail.html', context)

def teachers_attendance(request):
    return render(request, 'pages/teachers_attendance.html')

def admin_dash(request):
    return render(request, 'pages/admin_dash.html')

@login_required
def teacher_dash(request):
    user = request.user
    try:
        teacher = Teacher.objects.filter(user=user).first()
        classrooms = Classroom.objects.filter(teachers=teacher)
    
    except Teacher.DoesNotExist:
        teacher = None
        classrooms = None
    
    context = {
        "teacher": teacher,
        "classrooms": classrooms,
    }
    return render(request, 'pages/teacherdash.html', context)

def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    context = {
        'teacher': teacher,
    }
    return render(request, 'pages/teacher_detail.html', context)

@login_required
def add_performance(request):
    teacher = Teacher.objects.get(user=request.user)
    classrooms = Classroom.objects.filter(teachers=teacher)  
    students = Student.objects.filter(classrooms__in=classrooms)  
    subjects = Subject.objects.all()  
    assessment_components = AssessmentComponent.objects.all()

    context = {
        'students': students,
        'subjects': subjects,
        'assessment_components': assessment_components,
        'classrooms': classrooms,
    }
    return render(request, 'pages/add_performance_record.html', context)

def performance_records(request, student_id):
    student = Student.objects.get(id=student_id)
    performance_records = PerformanceRecord.objects.filter(student=student)
    subjects = student.subjects.all()
    
    context={
        "student":student, 
        "performance_records":performance_records, 
        "subjects":subjects
        
    }
    return render(request, 'pages/performance_records.html', context)

def attendance(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    attendance_records = AttendanceRecord.objects.filter(student=student).select_related('classroom').order_by('-date')
    classrooms = student.classrooms.all()
    
    context = {
        "student": student,
        "classrooms": classrooms, 
        "attendance_records": attendance_records
    }
    return render(request, 'pages/attendance.html', context)


def participation(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    participation_records = ParticipationRecord.objects.filter(student=student).select_related('classroom').order_by('-date')
    classrooms = student.classrooms.all()
    
    context = {
        "student": student,
        "classrooms": classrooms, 
        "participation_records": participation_records
    }
    return render(request, 'pages/participation.html', context)