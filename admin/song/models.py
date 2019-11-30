from django.db import models
from admin.genre.models import Genre
from admin.mood.models import Mood
from admin.artist.models import Artist

# Create your models here.

class Song(models.Model):

    song_name = models.CharField(max_length=100)
    song_des = models.CharField(max_length=250, default="This is a popular Song!")

    song_length = models.CharField(max_length=10)

    song_file = models.FileField(upload_to='songs/')

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.song_name