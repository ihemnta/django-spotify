from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from admin.artist.models import Artist
import re
# Create your views here.

@login_required(login_url = 'admin.login')
def add(request):
    return render(request, 'adminTemplates/artist/add.html')


@login_required(login_url = 'admin.login')
def save(request):
    if request.method == 'POST':

        name = request.POST['name']
        description = request.POST['description']

        if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', name):
            messages.error(request, "Enter a valid name!")
            return redirect("admin.artist.add")

        if not re.match('^[(a-z)?(A-Z)?\d?_?!?\-?\.?\,?\s?]+$', description):
            messages.error(request, "Enter a valid description!")
            return redirect("admin.artist.add")

        artist = Artist(artist_name=name, artist_des=description)

        artist.save()

        messages.success(request, "Data Added Successfully!")
        return redirect("admin.artist.index")

    else:
        return redirect("admin.artist.add")

@login_required(login_url = 'admin.login')
def index(request):

    data = Artist.objects.order_by('-id')
    return render(request, 'adminTemplates/artist/index.html', {'data':data})

@login_required(login_url = 'admin.login')
def delete(request, id):
    if request.method == 'GET':

        artist = Artist.objects.filter(pk=id)

        if not artist:
            messages.error(request, "No such record found!")
            return redirect('admin.artist.index')
        else:
            artist.delete()
            messages.success(request, "Record Deleted Successfully!")
            return redirect('admin.artist.index')

@login_required(login_url = 'admin.login')
def edit(request, id):
    if request.method == 'GET':

        artist = Artist.objects.filter(pk=id)

        if not artist:
            messages.error(request, "No such record found!")
            return redirect('admin.artist.index')
        else:
            artist = artist.get()
        
        return render(request, 'adminTemplates/artist/edit.html', {'artist':artist})

@login_required(login_url = 'admin.login')
def update(request, id):
    if request.method == 'POST':

        artist = Artist.objects.filter(pk=id)

        if not artist:
            messages.error(request, "No such record found!")
            return redirect('admin.artist.index')
        else:
            artist = artist.get()

        name = request.POST['name']
        description = request.POST['description']

        if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', name):
            messages.error(request, "Enter a valid name!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if not re.match('^[(a-z)?(A-Z)?\d?_?!?\-?\.?\,?\s?]+$', description):
            messages.error(request, "Enter a valid description!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        artist.artist_name = name
        artist.artist_des = description

        artist.save()

        messages.success(request, "Record Update Successfully!")

        return redirect('admin.artist.index')