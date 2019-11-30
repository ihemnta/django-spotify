from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from admin.genre.models import Genre
import re
# Create your views here.

@login_required(login_url = 'admin.login')
def add(request):
    return render(request, 'adminTemplates/genre/add.html')

@login_required(login_url = 'admin.login')
def save(request):
    if request.method == 'POST':

        name = request.POST['name']
        description = request.POST['description']

        if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', name):
            messages.error(request, "Enter a valid name!")
            return redirect("admin.genre.add")

        if not re.match('^[(a-z)?(A-Z)?\d?_?!?\-?\.?\,?\s?]+$', description):
            messages.error(request, "Enter a valid description!")
            return redirect("admin.genre.add")

        genre = Genre(genre_name=name, genre_des=description)

        genre.save()

        messages.success(request, "Data Added Successfully!")
        return redirect("admin.genre.index")

    else:
        return redirect("admin.genre.add")

@login_required(login_url = 'admin.login')
def index(request):

    data = Genre.objects.order_by('-id')
    return render(request, 'adminTemplates/genre/index.html', {'data':data})

@login_required(login_url = 'admin.login')
def delete(request, id):
    if request.method == 'GET':

        genre = Genre.objects.filter(pk=id)

        if not genre:
            messages.error(request, "No such record found!")
            return redirect('admin.genre.index')
        else:
            genre.delete()
            messages.success(request, "Record Deleted Successfully!")
            return redirect('admin.genre.index')

@login_required(login_url = 'admin.login')
def edit(request, id):
    if request.method == 'GET':

        genre = Genre.objects.filter(pk=id)

        if not genre:
            messages.error(request, "No such record found!")
            return redirect('admin.genre.index')
        else:
            genre = genre.get()
        
        return render(request, 'adminTemplates/genre/edit.html', {'genre':genre})

@login_required(login_url = 'admin.login')
def update(request, id):
    if request.method == 'POST':

        genre = Genre.objects.filter(pk=id)

        if not genre:
            messages.error(request, "No such record found!")
            return redirect('admin.genre.index')
        else:
            genre = genre.get()

        name = request.POST['name']
        description = request.POST['description']

        if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', name):
            messages.error(request, "Enter a valid name!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if not re.match('^[(a-z)?(A-Z)?\d?_?!?\-?\.?\,?\s?]+$', description):
            messages.error(request, "Enter a valid description!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        genre.genre_name = name
        genre.genre_des = description

        genre.save()

        messages.success(request, "Record Update Successfully!")

        return redirect('admin.genre.index')