from django.urls import path, include
from . import views

urlpatterns = [
    path('index', views.index, name='admin.user.index'),
    path('details/<int:id>', views.details, name='admin.user.details'),
    path('make-admin/', views.make_admin, name='admin.user.makeadmin'),
    # path('update/<int:id>', views.update, name='admin.genre.update'),
]