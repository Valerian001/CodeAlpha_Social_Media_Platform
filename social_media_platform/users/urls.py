from django.contrib import admin
from django.urls import path

from users import views as user_views

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('logout/', user_views.custom_logout, name='logout'),
    
    
]

