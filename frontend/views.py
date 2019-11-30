from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, logout, login as auth_login
from admin.homepage.models import Homepage
from admin.user.models import CustomUser
import re

def index(request):

    if request.user.is_authenticated:

        data = Homepage.objects.order_by('-id')

        return render(request, 'frontendTemplates/home/index.html', {'data':data})

    return render(request, 'frontendTemplates/home/index.html')

def signup(request):
    return render(request, 'frontendTemplates/signup/index.html')

def signup_post(request):

    if request.method == 'POST':

        if not 'name' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect("frontend.signup")

        if not 'email' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect("frontend.signup")

        if not 'password' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect("frontend.signup")

        if not 'number' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect("frontend.signup")

        if not 'gender' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect("frontend.signup")

        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        number = request.POST['number']
        gender = request.POST['gender']

        if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', name):
            messages.error(request, "Enter a valid name!")
            return redirect("frontend.signup")

        if not re.match(r"^[\w\.\+\-\_]+\@[\w\-]+\.[a-z]{2,3}$", email):
            messages.error(request, "Enter a valid Email!")
            return redirect('frontend.signup')

        if len(password) < 3:
            messages.error(request, "Your password is too short!")
            return redirect('frontend.signup')
        
        if not re.match('^[\d]{10,12}$', number):
            messages.error(request, "Invalid Phone Number!")
            return redirect("frontend.signup")

        if gender == "-1":
            messages.error(request, "Select a gender option!")
            return redirect("frontend.signup")

        try:
            usr = CustomUser(name=name, email=email, password=make_password(password), phone=number, gender=gender)
            usr.save()
        except Exception:
            messages.error(request, "The email already exists! Try a new one!")
            return redirect('frontend.signup')

        

        messages.success(request, "Successfully Registered!")
        return redirect('frontend.signup')
    else:
        messages.error(request, "Token Validation Failed!")
        return redirect('frontend.signup')

def login(request):
    return render(request, 'frontendTemplates/login/index.html')


def login_post(request):

    if request.method == 'POST':
        if not 'email' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect("frontend.login")

        if not 'password' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect("frontend.login")

        email = request.POST['email']
        password = request.POST['password']

        if not re.match(r"^[\w\.\+\-\_]+\@[\w\-]+\.[a-z]{2,3}$", email):
            messages.error(request, "Enter a valid Email!")
            return redirect('frontend.login')

        if len(password) < 3:
            messages.error(request, "Your password is too short!")
            return redirect('frontend.login')

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=email)

            if user.check_password(password):
                auth_login(request, user)
                return redirect('frontend.index')

            else:
                messages.error(request, "Invalid Password!")
                return redirect('frontend.login')

        except UserModel.DoesNotExist:
            messages.error(request, "Invalid Email!")
            return redirect('frontend.login')

    else:
        messages.error(request, "Invalid Token!")
        return redirect('frontend.login')

@login_required(login_url='frontend.login')
def logout_post(request):
    logout(request)
    return redirect('frontend.index')


        