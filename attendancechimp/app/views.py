from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import datetime

@csrf_exempt
def index(request):
    return render(request, 'app/index.html', {'todays_date': datetime.datetime.now().strftime('%B %d, %Y')})



@csrf_exempt
def handle_form(request):

    cname = request.POST['cname']
    cnum =  request.POST['cnum']

    print(cname, cnum)

    new_course = Course(cname, cnum)
    new_course.save()

    return render(request, 'app/index.html', {})

@csrf_exempt
def new_user(request):
    return render(request, 'app/create_user.html', {})