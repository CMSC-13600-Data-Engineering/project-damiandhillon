from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import datetime
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login
import logging
from django.shortcuts import redirect

@csrf_exempt
def index(request):
    if request.method == 'GET':
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
    if request.method == 'GET' and not request.user.is_authenticated:
        return render(request, 'app/new_user_page.html', {})
    raise PermissionDenied


@csrf_exempt
def create_user(request):
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_instructor = (request.POST.get("choice") == "instructor")

        if User.objects.filter(email=email).exists():
            return render(request, 'app/new_user_page.html', {'error': 'Email already in use'})

        # create the user
        user, _ = create_ac_user(username, email, password, is_instructor)
        # save the user
        user.save()
        

        # log the user in
        login(request, user)
        
        ## redirect to the logged_in page
        return redirect('logged_in')
                
    else:
        return render(request, 'app/new_user_page.html', {'error': 'Invalid request'})
    
def logout(request):
    logout(request)
    return redirect('index')