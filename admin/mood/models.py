from django.db import models

# Create your models here.


class Mood(models.Model):

    mood_name = models.CharField(max_length=50)
    mood_des = models.CharField(max_length=200, default="This is a Default Mood!")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mood_name