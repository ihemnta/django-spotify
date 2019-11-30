from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='frontend.webplayer.index'),
    path('<int:sid>', views.index_id, name='frontend.webplayer.index.id'),

    path('favorite/<int:sid>', views.favorite, name='frontend.webplayer.favorite'),

    path('genre/<int:sid>', views.genre, name='frontend.webplayer.genre'),
    path('genre/songs/<int:gid>/<int:sid>', views.genre_details, name='frontend.webplayer.genre.details'),

    path('mood/<int:sid>', views.mood, name='frontend.webplayer.mood'),
    path('mood/songs/<int:mid>/<int:sid>', views.mood_details, name='frontend.webplayer.mood.details'),

    path('artist/<int:sid>', views.artist, name='frontend.webplayer.artist'),
    path('artist/songs/<int:aid>/<int:sid>', views.artist_details, name='frontend.webplayer.artist.details'),

    path('category/<int:sid>', views.category, name='frontend.webplayer.category'),

    path('library/<int:sid>', views.library, name='frontend.webplayer.library'),

    path('search/<int:sid>', views.search, name='frontend.webplayer.search'),

    path('update-favorite', views.update_favorite, name='frontend.webplayer.update.favorite'),
]