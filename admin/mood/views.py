from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from admin.mood.models import Mood
import re
# Create your views here.

@login_required(login_url = 'admin.login')
def add(request):
    return render(request, 'adminTemplates/mood/add.html')

@login_required(login_url = 'admin.login')
def save(request):
    if request.method == 'POST':

        name = request.POST['name']
        description = request.POST['description']

        if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', name):
            messages.error(request, "Enter a valid name!")
            return redirect("admin.mood.add")

        if not re.match('^[(a-z)?(A-Z)?\d?_?!?\-?\.?\,?\s?]+$', description):
            messages.error(request, "Enter a valid description!")
            return redirect("admin.mood.add")

        mood = Mood(mood_name=name, mood_des=description)

        mood.save()

        messages.success(request, "Data Added Successfully!")
        return redirect("admin.mood.index")

    else:
        return redirect("admin.mood.add")

@login_required(login_url = 'admin.login')
def index(request):

    data = Mood.objects.order_by('-id')
    return render(request, 'adminTemplates/mood/index.html', {'data':data})

@login_required(login_url = 'admin.login')
def delete(request, id):
    if request.method == 'GET':

        mood = Mood.objects.filter(pk=id)

        if not mood:
            messages.error(request, "No such record found!")
            return redirect('admin.mood.index')
        else:
            mood.delete()
            messages.success(request, "Record Deleted Successfully!")
            return redirect('admin.mood.index')


@login_required(login_url = 'admin.login')
def edit(request, id):
    if request.method == 'GET':

        mood = Mood.objects.filter(pk=id)

        if not mood:
            messages.error(request, "No such record found!")
            return redirect('admin.mood.index')
        else:
            mood = mood.get()
        
        return render(request, 'adminTemplates/mood/edit.html', {'mood':mood})


@login_required(login_url = 'admin.login')
def update(request, id):
    if request.method == 'POST':

        mood = Mood.objects.filter(pk=id)

        if not mood:
            messages.error(request, "No such record found!")
            return redirect('admin.mood.index')
        else:
            mood = mood.get()

        name = request.POST['name']
        description = request.POST['description']

        if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', name):
            messages.error(request, "Enter a valid name!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if not re.match('^[(a-z)?(A-Z)?\d?_?!?\-?\.?\,?\s?]+$', description):
            messages.error(request, "Enter a valid description!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        mood.mood_name = name
        mood.mood_des = description

        mood.save()

        messages.success(request, "Record Update Successfully!")

        return redirect('admin.mood.index')