'''Basic test harness to make sure all of the functionality works
'''

# Some boilerplate code to get things running
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendancechimp.settings")
django.setup()
print("[1] Initializing Django successful")


# import data from models to test
from app.models import *
print("[2] Import from models.py successful")


# do some clean up
from django.contrib.auth.models import User
for user in User.objects.all():
    user.delete()
print("[3] Deleted all users")

# create some fake data
# create a test instructor
ts_django , ts_up = create_ac_user("Taylor Swift", "ts@gmail.com", "shakeitoff", True)
# create a test student
bb_django , bb_up = create_ac_user("Bob Bar", "bb@gmail.com", "1234", False)
assert(User.objects.count() == 2)
assert(UniversityPerson.objects.count() == 2)
print("[4] User Creation successful")

# create a test course
start = "10:00:00"
end = "11:00:00"
course = create_course("Intro to Data Eng", ts_up, ["M", "W", "F"], start, end)
assert(Course.objects.count() == 1)
print("[5] Course Creation successful")

# create a qr code
code = create_qr_code(course)
assert(QRCode.objects.count() == 1)
print("[5] QRCode Creation successful with code=",code.code)

# create qr code upload
upload = process_upload(course, bb_up, None) 
assert(QRCodeUpload.objects.count() == 1)
print("[6] QRCodeUpload successful by student = ",upload.student.user.username)
