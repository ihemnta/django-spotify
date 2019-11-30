from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from admin.homepage.models import Homepage
from admin.song.models import Song
from admin.user.models import CustomUser
from admin.favorite.models import Favorite
from admin.genre.models import Genre
from admin.mood.models import Mood
from admin.artist.models import Artist
import random
import json
import re

# Create your views here.

def find_song(sid):
    
    song = Song.objects.filter(pk=sid)

    if not song:
        return False
    else:
        song = song.get()

    song_ids = Song.objects.values_list('id', flat=True)

    sid_index = list(song_ids).index(sid)

    # print("INDEX of Curr Song : " + str(sid_index))

    # print(song_ids)

    if sid_index == 0:
        
        prev_id = '-1'
        next_id = str(song_ids[sid_index+1])

    elif sid_index == len(song_ids) - 1:
        
        prev_id = str(song_ids[sid_index-1])
        next_id = '-1'

    else:
        prev_id = str(song_ids[sid_index-1])
        next_id = str(song_ids[sid_index+1])

    # print(song.id)
    # print(prev_id)
    # print(next_id)

    return song, prev_id, next_id



def random_song_id():
    song_ids = Song.objects.values_list('id', flat=True)

    return random.choice(list(song_ids))

@login_required(login_url='frontend.login')
def index(request):
    return redirect('frontend.webplayer.index.id', sid=random_song_id())

@login_required(login_url='frontend.login')
def index_id(request, sid):

    data = Homepage.objects.all()

    if find_song(sid):

        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        return redirect('frontend.login')
    else:
        user = user.get()

    fav = Favorite.objects.filter(song=song, user=user)

    if not fav:
        fav = False
    else:
        fav = True

    return render(request, 'frontendTemplates/webplayer/index.html', {'data':data, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})


@login_required(login_url='frontend.login')
def favorite(request, sid):

    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        return redirect('frontend.login')
    else:
        user = user.get()

    data = Favorite.objects.filter(user=user)

    if find_song(sid):

        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    fav = Favorite.objects.filter(song=song, user=user)

    if not fav:
        fav = False
    else:
        fav = True

    return render(request, 'frontendTemplates/webplayer/favorite.html', {'data':data, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})


@login_required(login_url='frontend.login')
def genre(request, sid):

    data = Genre.objects.all()
    
    # Grabbing Logged In User Data
    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        return redirect('frontend.login')
    else:
        user = user.get()

    # Grabbing Current Song Data
    if find_song(sid):

        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    # Grabbing if the song is in favorite list
    fav = Favorite.objects.filter(song=song, user=user)

    if not fav:
        fav = False
    else:
        fav = True

    return render(request, 'frontendTemplates/webplayer/genre.html', {'data':data, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})


@login_required(login_url='frontend.login')
def genre_details(request, gid, sid):
    
    genre = Genre.objects.filter(pk=gid)

    if not genre:

        genre_songs = Song.objects.all()

    else:
        genre = genre.get()

        genre_songs = Song.objects.filter(genre=genre)

    # Grabbing Logged In User Data
    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        return redirect('frontend.login')
    else:
        user = user.get()

    # Grabbing Current Song Data
    if find_song(sid):

        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    # Grabbing if the song is in favorite list
    fav = Favorite.objects.filter(song=song, user=user)

    if not fav:
        fav = False
    else:
        fav = True

    return render(request, 'frontendTemplates/webplayer/genre_details.html', {'genre':genre, 'genre_songs':genre_songs, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})


@login_required(login_url='frontend.login')
def mood(request, sid):
    data = Mood.objects.all()
    
    # Grabbing Logged In User Data
    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        return redirect('frontend.login')
    else:
        user = user.get()

    # Grabbing Current Song Data
    if find_song(sid):

        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    # Grabbing if the song is in favorite list
    fav = Favorite.objects.filter(song=song, user=user)

    if not fav:
        fav = False
    else:
        fav = True

    return render(request, 'frontendTemplates/webplayer/mood.html', {'data':data, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})


@login_required(login_url='frontend.login')
def mood_details(request, mid, sid):
    
    mood = Mood.objects.filter(pk=mid)

    if not mood:

        mood_songs = Song.objects.all()

    else:
        mood = mood.get()

        mood_songs = Song.objects.filter(mood=mood)

    # Grabbing Logged In User Data
    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        return redirect('frontend.login')
    else:
        user = user.get()

    # Grabbing Current Song Data
    if find_song(sid):

        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    # Grabbing if the song is in favorite list
    fav = Favorite.objects.filter(song=song, user=user)

    if not fav:
        fav = False
    else:
        fav = True

    return render(request, 'frontendTemplates/webplayer/mood_details.html', {'mood':mood, 'mood_songs':mood_songs, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})


@login_required(login_url='frontend.login')
def artist(request, sid):
    data = Artist.objects.all()
    
    # Grabbing Logged In User Data
    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        return redirect('frontend.login')
    else:
        user = user.get()

    # Grabbing Current Song Data
    if find_song(sid):

        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    # Grabbing if the song is in favorite list
    fav = Favorite.objects.filter(song=song, user=user)

    if not fav:
        fav = False
    else:
        fav = True

    return render(request, 'frontendTemplates/webplayer/artist.html', {'data':data, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})



@login_required(login_url='frontend.login')
def artist_details(request, aid, sid):
    
    artist = Artist.objects.filter(pk=aid)

    if not artist:

        artist_songs = Song.objects.all()

    else:
        artist = artist.get()

        artist_songs = Song.objects.filter(artist=artist)

    # Grabbing Logged In User Data
    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        return redirect('frontend.login')
    else:
        user = user.get()

    # Grabbing Current Song Data
    if find_song(sid):

        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    # Grabbing if the song is in favorite list
    fav = Favorite.objects.filter(song=song, user=user)

    if not fav:
        fav = False
    else:
        fav = True

    return render(request, 'frontendTemplates/webplayer/artist_details.html', {'artist':artist, 'artist_songs':artist_songs, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})


@login_required(login_url='frontend.login')
def category(request, sid):

    homepage = Homepage.objects.all()

    genre = Genre.objects.all()

    mood = Mood.objects.all()

    artist = Artist.objects.all()
    
    # Grabbing Logged In User Data
    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        return redirect('frontend.login')
    else:
        user = user.get()

    # Grabbing Current Song Data
    if find_song(sid):

        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    # Grabbing if the song is in favorite list
    fav = Favorite.objects.filter(song=song, user=user)

    if not fav:
        fav = False
    else:
        fav = True

    return render(request, 'frontendTemplates/webplayer/category.html', {'homepage':homepage, 'genre':genre, 'mood':mood, 'artist':artist, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})


@login_required(login_url='frontend.login')
def library(request, sid):
    data = Song.objects.all()
    
    # Grabbing Logged In User Data
    user = CustomUser.objects.filter(pk=request.user.id)

    if not user:
        return redirect('frontend.login')
    else:
        user = user.get()

    # Grabbing Current Song Data
    if find_song(sid):

        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    # Grabbing if the song is in favorite list
    fav = Favorite.objects.filter(song=song, user=user)

    if not fav:
        fav = False
    else:
        fav = True

    return render(request, 'frontendTemplates/webplayer/library.html', {'data':data, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})


@login_required(login_url='frontend.login')
def search(request, sid):

    if request.method == 'GET':

        if 'search' in request.GET.keys():
            
            keyword = request.GET['search']

            if not re.match('^[(a-z)?(A-Z)?\d?_?\-?\.?\,?\s?]+$', keyword):
                # Grabbing Logged In User Data
                user = CustomUser.objects.filter(pk=request.user.id)

                if not user:
                    return redirect('frontend.login')
                else:
                    user = user.get()

                # Grabbing Current Song Data
                if find_song(sid):

                    song, prev_id, next_id = find_song(sid)
                else:
                    song, prev_id, next_id = find_song(random_song_id())

                # Grabbing if the song is in favorite list
                fav = Favorite.objects.filter(song=song, user=user)

                if not fav:
                    fav = False
                else:
                    fav = True

                return render(request, 'frontendTemplates/webplayer/search.html', {'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})

            else:
                
                lookups = Q(song_name__icontains=keyword) | Q(artist__artist_name__icontains=keyword) | Q(mood__mood_name__icontains=keyword) | Q(genre__genre_name__icontains=keyword)

                song_data = Song.objects.filter(lookups)

                # Grabbing Logged In User Data
                user = CustomUser.objects.filter(pk=request.user.id)

                if not user:
                    return redirect('frontend.login')
                else:
                    user = user.get()

                # Grabbing Current Song Data
                if find_song(sid):

                    song, prev_id, next_id = find_song(sid)
                else:
                    song, prev_id, next_id = find_song(random_song_id())

                # Grabbing if the song is in favorite list
                fav = Favorite.objects.filter(song=song, user=user)

                if not fav:
                    fav = False
                else:
                    fav = True

                return render(request, 'frontendTemplates/webplayer/search.html', {'song_data':song_data, 'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})


        else:

            # Grabbing Logged In User Data
            user = CustomUser.objects.filter(pk=request.user.id)

            if not user:
                return redirect('frontend.login')
            else:
                user = user.get()

            # Grabbing Current Song Data
            if find_song(sid):

                song, prev_id, next_id = find_song(sid)
            else:
                song, prev_id, next_id = find_song(random_song_id())

            # Grabbing if the song is in favorite list
            fav = Favorite.objects.filter(song=song, user=user)

            if not fav:
                fav = False
            else:
                fav = True

            return render(request, 'frontendTemplates/webplayer/search.html', {'song':song, 'prev_id':prev_id, 'next_id':next_id, 'fav':fav})





@login_required(login_url='frontend.login')
def update_favorite(request):
    if request.is_ajax():

        if not 'action' in request.POST.keys():
            return HttpResponse(json.dumps({'key':'0', 'msg':'Parameters are missing!'}))

        if not 'sid' in request.POST.keys():
            return HttpResponse(json.dumps({'key':'0', 'msg':'Parameters are missing!'}))

        user = CustomUser.objects.filter(pk=request.user.id)

        if not user:
            return redirect('frontend.login')
        else:
            user = user.get()

        if request.POST['action'] == '1':
            
            song = Song.objects.filter(pk=request.POST['sid'])

            if not song:
                return HttpResponse(json.dumps({'key':'0', 'msg':'Invalid Song ID!'}))
            else:
                song = song.get()

            fav = Favorite.objects.filter(user=user, song=song)

            if fav:
                return HttpResponse(json.dumps({'key':'0', 'msg':'Already added to favorites!'}))
            else:
                fav = Favorite(user=user, song=song)

                fav.save()

                return HttpResponse(json.dumps({'key':'1', 'msg':'Added to Favorites!'}))

        elif request.POST['action'] == '2':

            song = Song.objects.filter(pk=request.POST['sid'])

            if not song:
                return HttpResponse(json.dumps({'key':'0', 'msg':'Invalid Song ID!'}))
            else:
                song = song.get()

            fav = Favorite.objects.filter(user=user, song=song)

            if not fav:
                return HttpResponse(json.dumps({'key':'0', 'msg':'Not in Favorites'}))
            else:
                fav.delete()
            
            return HttpResponse(json.dumps({'key':'1', 'msg':'Removed from Favorites!'}))
            
        else:
            return HttpResponse(json.dumps({'key':'0', 'msg':'Invalid Value!'}))