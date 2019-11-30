from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='frontend.index'),
    path('signup/', views.signup, name='frontend.signup'),
    path('signup/post', views.signup_post, name='frontend.signup.post'),
    path('login/', views.login, name='frontend.login'),
    path('login/post', views.login_post, name='frontend.login.post'),
    path('logout/', views.logout_post, name='frontend.logout'),
    path('accounts/', include('frontend.account.urls')),
    path('webplayer/', include('frontend.webplayer.urls')),
]