from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home,name='home'),
    path('detect', views.detect, name='detect'),
    path('contact', views.contact, name="contact"),
    path('getintouch', views.getintouch, name='getintouch'),
    path('news', views.news, name='news'),
    path('upload/', views.upload_file, name='upload_file'),
]