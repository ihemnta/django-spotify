from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from admin.song.models import Song
from admin.homepage.models import Homepage
import re
# Create your views here.

@login_required(login_url = 'admin.login')
def add(request):

    data = Song.objects.all()

    return render(request, 'adminTemplates/homepage/add.html', {'data':data})

@login_required(login_url = 'admin.login')
def save(request):
    if request.method == 'POST':

        if not 'title' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect("admin.homepage.add")

        if not 'song' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return redirect("admin.homepage.add")

        title = request.POST['title']
        song = request.POST['song']

        if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', title):
            messages.error(request, "Enter a valid name!")
            return redirect("admin.homepage.add")

        if song == "-1":
            messages.error(request, "Select A Song!")
            return redirect("admin.homepage.add")

        song = Song.objects.filter(pk=song)
        if not song:
            messages.error(request, "Select a valid Song!")
            return redirect("admin.homepage.add")
        else:
            song = song.get()



        homepage = Homepage(title=title, song=song)

        homepage.save()

        messages.success(request, "Data Added Successfully!")
        return redirect("admin.homepage.index")

    else:
        return redirect("admin.homepage.add")


@login_required(login_url = 'admin.login')
def index(request):

    data = Homepage.objects.order_by('-id')
    return render(request, 'adminTemplates/homepage/index.html', {'data':data})


@login_required(login_url = 'admin.login')
def delete(request, id):
    if request.method == 'GET':

        homepage = Homepage.objects.filter(pk=id)

        if not homepage:
            messages.error(request, "No such record found!")
            return redirect('admin.homepage.index')
        else:
            homepage.delete()
            messages.success(request, "Record Deleted Successfully!")
            return redirect('admin.homepage.index')


@login_required(login_url = 'admin.login')
def edit(request, id):
    if request.method == 'GET':

        homepage = Homepage.objects.filter(pk=id)

        data = Song.objects.all()

        if not homepage:
            messages.error(request, "No such record found!")
            return redirect('admin.homepage.index')
        else:
            homepage = homepage.get()
        
        return render(request, 'adminTemplates/homepage/edit.html', {'homepage':homepage, 'data':data})



@login_required(login_url = 'admin.login')
def update(request, id):
    if request.method == 'POST':

        homepage = Homepage.objects.filter(pk=id)

        if not homepage:
            messages.error(request, "No such record found!")
            return redirect('admin.homepage.index')
        else:
            homepage = homepage.get()

        
        if not 'title' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if not 'song' in request.POST.keys():
            messages.error(request, "Parameters are missing!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        title = request.POST['title']
        song = request.POST['song']

        if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', title):
            messages.error(request, "Enter a valid title!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if song == "-1":
            messages.error(request, "Select A Song!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        song = Song.objects.filter(pk=song)
        if not song:
            messages.error(request, "Select a valid Song!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            song = song.get()


        homepage.title = title
        homepage.song = song

        homepage.save()

        messages.success(request, "Record Update Successfully!")

        return redirect('admin.homepage.index')