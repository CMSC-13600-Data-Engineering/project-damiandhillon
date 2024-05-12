import os
import django
import pytz
from datetime import datetime, timedelta

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendancechimp.settings")
django.setup()

from app.models import create_ac_user, create_course, create_qr_code, process_upload
from app.models import UniversityPerson, Course, QRCode, QRCodeUpload
from django.contrib.auth.models import User

# Clean up existing data
User.objects.all().delete()
UniversityPerson.objects.all().delete()
Course.objects.all().delete()
QRCode.objects.all().delete()
QRCodeUpload.objects.all().delete()

# Create test data
# Create a new instructor
instructor_django, instructor_up = create_ac_user("John Doe", "john@example.com", "password", True)
# Create a new student
student_django, student_up = create_ac_user("Jane Smith", "jane@example.com", "password", False)

# Create a new course
start_time = "09:00:00"
end_time = "10:00:00"
course = create_course("Advanced Python", instructor_up, ["M", "W", "F"], start_time, end_time)
print(f"Created course with ID: {course.auto_increment_id}")

# Function to generate the next occurrence of a given weekday
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    result_date = d + timedelta(days_ahead)
    print(f"Next {weekday} from {d} is {result_date}")
    return result_date

# Create QR code uploads at valid times
def adjust_to_next_weekday(d, target_weekday, hour, minute):
    days_ahead = (target_weekday - d.weekday() + 7) % 7
    result_date = d + timedelta(days_ahead)
    result_date = result_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    print(f"Adjusting {d} to next {target_weekday}: {result_date}")
    return result_date

# Ensure valid upload times based on the course schedule
current_time = datetime.now(pytz.utc)

valid_upload_times = [
    adjust_to_next_weekday(current_time, 0, 9, 15),  # Next Monday at 09:15
    adjust_to_next_weekday(current_time, 2, 9, 30),  # Next Wednesday at 09:30
]

# Invalid upload time (Sunday)
invalid_upload_time = adjust_to_next_weekday(current_time, 6, 15, 0)  # Next Sunday at 15:00

# Create QR code uploads
for upload_time in valid_upload_times:
    upload = QRCodeUpload(course=course, student=student_up, uploaded=upload_time)
    upload.save()

# Create invalid upload
upload_invalid = QRCodeUpload(course=course, student=student_up, uploaded=invalid_upload_time)
upload_invalid.save()

print("Users:", User.objects.all())
print("UniversityPersons:", UniversityPerson.objects.all())
print("Courses:", Course.objects.all())
print("QRCodeUploads:", QRCodeUpload.objects.all())

# Print detailed information
print("\nDetailed Information:")
for person in UniversityPerson.objects.all():
    print(f"ID: {person.auto_increment_id}, Username: {person.user.username}, Is Instructor: {person.is_instructor}")

for course in Course.objects.all():
    print(f"ID: {course.auto_increment_id}, Name: {course.name}, Instructor: {course.instructor.user.username}")

for upload in QRCodeUpload.objects.all():
    print(f"ID: {upload.auto_increment_id}, Student: {upload.student.user.username}, Course: {upload.course.name}, Uploaded: {upload.uploaded}")
