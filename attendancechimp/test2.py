import os
import django
from datetime import datetime, timedelta
import pytz

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendancechimp.settings")
django.setup()

from app.models import create_ac_user, create_course, create_qr_code, UniversityPerson, Course, QRCode, QRCodeUpload
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

# Clean up existing data
User.objects.all().delete()
UniversityPerson.objects.all().delete()
Course.objects.all().delete()
QRCode.objects.all().delete()
QRCodeUpload.objects.all().delete()

# Create instructors and their courses
instructor1, up_instructor1 = create_ac_user("John Doe", "john@example.com", "password", True)
instructor2, up_instructor2 = create_ac_user("Jane Bar", "jane@example.com", "password", True)
course1 = create_course("Calculus 101", up_instructor1, ["M", "W", "F"], "08:00:00", "09:30:00")
print(f"Created course '{course1.name}' with ID: {course1.auto_increment_id}")  # Print course 1 ID
course2 = create_course("Physics 101", up_instructor2, ["Tu", "Th"], "10:00:00", "11:30:00")
print(f"Created course '{course2.name}' with ID: {course2.auto_increment_id}")  # Print course 1 ID


# Create 20 students
students = []
for i in range(30):
    student, up_student = create_ac_user(f"Student{i+1}", f"student{i+1}@example.com", "password", False)
    students.append(up_student)

# Create QR codes for each course
qr_code1 = create_qr_code(course1)
qr_code2 = create_qr_code(course2)

# Function to generate the next occurrence of a given weekday
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

# Create valid and invalid uploads directly, using QRCodeUpload
current_time = datetime.now(pytz.utc)
dummy_image = SimpleUploadedFile("dummy.jpg", b"dummy data")

# Valid uploads for John Doe's course
for student in students[:10]:
    upload_time = next_weekday(current_time, 0)  # Next Monday
    upload_time = upload_time.replace(hour=8, minute=30)  # During the course time
    QRCodeUpload(course=course1, student=student, image=dummy_image, uploaded=upload_time).save()

# Valid uploads for Jane Bar's course
for student in students[10:20]:
    upload_time = next_weekday(current_time, 1)  # Next Tuesday
    upload_time = upload_time.replace(hour=10, minute=45)  # During the course time
    QRCodeUpload(course=course2, student=student, image=dummy_image, uploaded=upload_time).save()

# Invalid uploads for remaining students
for student in students[20:]:
    upload_time = next_weekday(current_time, 6)  # Next Sunday, invalid time
    QRCodeUpload(course=course1 if i % 2 == 0 else course2, student=student, image=dummy_image, uploaded=upload_time).save()

print("Test data setup complete.")
