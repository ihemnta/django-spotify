from django.urls import path, include
from . import views

urlpatterns = [
    path('add', views.add, name='admin.artist.add'),
    path('save', views.save, name='admin.artist.save'),
    path('index', views.index, name='admin.artist.index'),
    path('delete/<int:id>', views.delete, name='admin.artist.delete'),
    path('edit/<int:id>', views.edit, name='admin.artist.edit'),
    path('update/<int:id>', views.update, name='admin.artist.update'),
]