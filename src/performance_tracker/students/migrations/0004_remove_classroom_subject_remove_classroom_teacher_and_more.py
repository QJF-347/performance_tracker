# Generated by Django 5.1.6 on 2025-03-05 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_classroom_teacher_attendancerecord_classroom_and_more'),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='teacher',
        ),
        migrations.AddField(
            model_name='classroom',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='classroom',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='classrooms', to='students.subject'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='teachers',
            field=models.ManyToManyField(related_name='classrooms', to='teachers.teacher'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='classrooms', to='students.student'),
        ),
    ]
