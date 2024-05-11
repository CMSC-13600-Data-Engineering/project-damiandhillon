'''Basic test harness to make sure all of the functionality works
'''

# Some boilerplate code to get things running
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendancechimp.settings")
django.setup()

# create a test user
up, user = create_ac_user("Taylor Swift", "ts@gmail.com", "shakeitoff", True)

# create a test course
start = strftime("%H", "10")
end = strftime("%H", "11")
create_course("Intro to Data Eng", up, ["M", "W", "F"], start, end)