from django.urls import path, include
from . import views

urlpatterns = [
    path('add', views.add, name='admin.mood.add'),
    path('save', views.save, name='admin.mood.save'),
    path('index', views.index, name='admin.mood.index'),
    path('delete/<int:id>', views.delete, name='admin.mood.delete'),
    path('edit/<int:id>', views.edit, name='admin.mood.edit'),
    path('update/<int:id>', views.update, name='admin.mood.update'),
]