from django.db import models
from django.utils import timezone

class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Should be hashed

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Should be hashed

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    number = models.CharField(max_length=5)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')

class Lecture(models.Model):
    lecture_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=256)
    lecture_date = models.DateTimeField()

class QRCode(models.Model):
    qr_code_id = models.AutoField(primary_key=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='qr_codes')
    code = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE, related_name='attendances')
    timestamp = models.DateTimeField(default=timezone.now)
    upload = models.ImageField(upload_to='attendance_uploads/')
    verified = models.BooleanField(default=False)
