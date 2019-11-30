from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse
from admin.user.models import CustomUser
import re
import json


# Create your views here.
@login_required(login_url='frontend.login')
def index(request):

    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        messages.error(request, "Log In First!")
        return redirect('frontend.login')

    else:
        user = user.get()

    return render(request, 'frontendTemplates/account/index.html', {'user':user})



@login_required(login_url='frontend.login')
def edit(request):

    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        messages.error(request, "Log In First!")
        return redirect('frontend.login')

    else:
        user = user.get()

    return render(request, 'frontendTemplates/account/edit.html', {'user':user})


@login_required(login_url='frontend.login')
def update(request):

    if request.method == "POST":

        user = CustomUser.objects.filter(pk=request.user.id)

        if not user:
            messages.error(request, "Log In First!")
            return redirect('frontend.login')

        else:
            user = user.get()

        if not 'name' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect('frontend.account.edit')

        if not 'email' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect('frontend.account.edit')

        if not 'gender' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect('frontend.account.edit')

        if not 'mobile' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect('frontend.account.edit')

        name = request.POST['name']
        email = request.POST['email']
        gender = request.POST['gender']
        mobile = request.POST['mobile']

        if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', name):
            messages.error(request, "Enter a valid name!")
            return redirect("frontend.account.edit")

        if not re.match(r"^[\w\.\+\-\_]+\@[\w\-]+\.[a-z]{2,3}$", email):
            messages.error(request, "Enter a valid Email!")
            return redirect('frontend.account.edit')

        if not re.match('^[\d]{10,12}$', mobile):
            messages.error(request, "Invalid Phone Number!")
            return redirect("frontend.account.edit")

        user.name = name
        user.email = email
        user.gender = gender
        user.phone = mobile

        user.save()

        messages.success(request, "Profile Updated!")
        return redirect("frontend.account.index")
    else:
        return redirect("frontend.account.edit")


@login_required(login_url='frontend.login')
def edit_pass(request):

    return render(request, 'frontendTemplates/account/edit_pass.html')



@login_required(login_url='frontend.login')
def update_pass(request):

    if request.method == "POST":

        if not 'cpass' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect('frontend.account.edit.pass')

        if not 'npass' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect('frontend.account.edit.pass')

        if not 'conpass' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect('frontend.account.edit.pass')

        cpass = request.POST['cpass']
        npass = request.POST['npass']
        conpass = request.POST['conpass']

        if((len(cpass) < 3) or (len(npass) < 3) or (len(conpass) < 3)):
            messages.error(request, "Passwords should not be less than 3 characters!")
            return redirect('frontend.account.edit.pass')

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=request.user.id)

            if user.check_password(cpass):

                if npass != conpass:
                    messages.error(request, "Confirm Password doesn't match with New Password!")
                    return redirect('frontend.account.edit.pass')

                user.password = make_password(npass)
                user.save()

                auth_login(request, user)

                messages.success(request, "Password Changed!")
                return redirect('frontend.account.edit.pass')

            else:
                messages.error(request, "Current Password Doesn't Match!")
                return redirect('frontend.account.edit.pass')

        except UserModel.DoesNotExist:
            messages.error(request, "Log In First!")
            return redirect('frontend.login')

@login_required(login_url='frontend.login')
def privacy(request):

    return render(request, 'frontendTemplates/account/privacy.html')

@login_required(login_url='frontend.login')
def subscription(request):

    return render(request, 'frontendTemplates/account/subscription.html')


@login_required(login_url='frontend.login')
def change_profile_pic(request):
    if request.is_ajax():
        if not 'file' in request.FILES.keys():
            return HttpResponse(json.dumps({'key':'0', 'msg':'No file selected!'}))
        if not request.FILES['file'].name.split('.')[-1].lower() in ['jpg','png','jpeg']:
            return HttpResponse(json.dumps({'key':'0', 'msg':'Invalid File Type!'}))

        user = CustomUser.objects.filter(pk=request.user.id)

        if not user:
            messages.error(request, "Log In First!")
            return redirect('frontend.login')
        else:
            user = user.get()

        if 'team.jpg' in str(user.profile_pic):

            user.profile_pic = request.FILES['file']

            user.save()
        else:
            user.profile_pic.delete()

            user.profile_pic = request.FILES['file']

            user.save()

        return HttpResponse(json.dumps({'key':'1', 'msg':'Profile Picture Updated!'}))
        
