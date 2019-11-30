from django.shortcuts import render

from rest_framework import viewsets

from .serializer import SongSerializer
from admin.song.models import Song

class SongViewSets(viewsets.ModelViewSet):

    queryset = Song.objects.all().order_by('id')
    serializer_class = SongSerializer
