'''SOLUTIONS. These are solutions that might help you think about
the problem in a different way. Note the simplicity of the models
compared to some of what you might have implemented. We'll walk 
through all of this step-by-step. 
'''

# import to get the models class  from django
from django.db import models

# get access to django users
from django.contrib.auth.models import User

# some stuff to get the QR code working easier
from django.utils.crypto import get_random_string


class UniversityPerson(models.Model):
    """This model describes a university person, either a student
    or an instructor. It contains all of the necessary data that
    might identify such a person.

    Note: We link this entity to the Django user model so we only
    need to store information unique to a "UniversityPerson" above
    and beyond a simple user.
    """

    # an auto incrementing id
    auto_increment_id = models.AutoField(primary_key=True)

    # is an instructor or student?
    is_instructor = models.BooleanField(null=False)

    # relate to django auth user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# for each model, I like to wrap it in a simple helper function
# for example for the user model, when creating a user we create
# two users one university person and one django user.
def create_ac_user(name, email, password, is_instructor):
    """Creates an ac user and a corresponding django user"""

    # first create django user
    user = User.objects.create_user(name, email, password)
    user.save()

    # then create ac user
    up = UniversityPerson(is_instructor=is_instructor, user=user)
    up.save()

    # return both users
    return user, up


class Course(models.Model):
    """A course represents a single course using attendancechimp. A course
    stores a reference to the instructor as well as the times/days of the
    week that it meets."""

    # an internal unique id
    auto_increment_id = models.AutoField(primary_key=True)

    # a course name
    name = models.CharField(max_length=128)

    # foreign key to instructor
    instructor = models.ForeignKey(UniversityPerson, on_delete=models.CASCADE)

    # class time start and end
    class_start = models.TimeField()
    class_end = models.TimeField()

    # class days
    m_class = models.BooleanField(default=False)
    tu_class = models.BooleanField(default=False)
    w_class = models.BooleanField(default=False)
    th_class = models.BooleanField(default=False)
    f_class = models.BooleanField(default=False)


# let's spec out the basic functionality of a course
def create_course(name, instructor, days, start, end):
    """Creates an ac user and a corresponding django user"""
    course = Course(name=name, instructor=instructor, class_start=start, class_end=end)

    # handles course meetings
    for d in days:
        if d == "M":
            course.m_class = True

        if d == "Tu":
            course.tu_class = True

        if d == "W":
            course.w_class = True

        if d == "Th":
            course.th_class = True

        if d == "F":
            course.f_class = True

    course.save()

    return course


class QRCode(models.Model):
    """A qr code is tied to a particular lecture. Note this object just defines the
    QR code does not contain any image data.
    """

    # an internal unique id
    auto_increment_id = models.AutoField(primary_key=True)

    # linked to a course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # code
    code = models.CharField(max_length=32)

    # this is a trick to automatically generate a random
    # string on save
    def save(self, *args, **kwargs):
        self.code = get_random_string(length=32)
        super(QRCode, self).save(*args, **kwargs)


# this is the functionality to create a qr code
def create_qr_code(course):
    qrcode = QRCode(course=course)
    qrcode.save()
    return qrcode


class QRCodeUpload(models.Model):
    """This model represents a particular qrcode upload from a student."""

    # an internal unique id
    auto_increment_id = models.AutoField(primary_key=True)

    # linked to a course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # linked to a student
    student = models.ForeignKey(UniversityPerson, on_delete=models.CASCADE)

    # data
    image = models.ImageField(upload_to="data")

    # time stamp on upload
    uploaded = models.DateTimeField(auto_now_add=True)
    # time stamp on upload for TESTING PURPOSES
    # uploaded = models.DateTimeField()

import pytz
# this is the functionality to process an upload
def process_upload(course, student, image):
    now = datetime.now(pytz.utc)
    upload = QRCodeUpload(course=course, student=student, image=image, uploaded=now)
    upload.save()
    return upload

from datetime import datetime

def getUploadsForCourse(course_id):
    """Returns all valid QRCodeUpload objects for a given course ID."""
    print(f"Getting uploads for course ID: {course_id}")

    # Validate the course ID
    try:
        course = Course.objects.get(auto_increment_id=course_id)
        print(f"Course found: {course.name}")
    except Course.DoesNotExist:
        print("Course does not exist")
        return []

    # Get all QRCodeUpload objects for the course
    uploads = QRCodeUpload.objects.filter(course=course)
    print(f"Total uploads found: {uploads.count()}")

    # Filter valid uploads
    valid_uploads = []
    for upload in uploads:
        upload_day = upload.uploaded.strftime('%A')[:2]
        upload_time = upload.uploaded.time()
        print(f"Checking upload: {upload.student.user.username} at {upload.uploaded} (day: {upload_day}, time: {upload_time})")

        if (upload_day == 'Mo' and course.m_class) or \
           (upload_day == 'Tu' and course.tu_class) or \
           (upload_day == 'We' and course.w_class) or \
           (upload_day == 'Th' and course.th_class) or \
           (upload_day == 'Fr' and course.f_class):
            
            if course.class_start <= upload_time <= course.class_end:
                valid_uploads.append(upload)
                print(f"Valid upload: {upload.student.user.username} at {upload.uploaded}")

    print(f"Total valid uploads: {len(valid_uploads)}")
    return valid_uploads

