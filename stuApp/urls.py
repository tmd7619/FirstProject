
from django.contrib import admin
from django.urls import path, include
from stuApp import views

app_name= 'stuApp'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register2'),
    path('login/', views.login, name='login2'),
    path('registerForm2/', views.registerForm2, name='registerForm2'),
    path('loginForm/', views.loginForm, name='loginForm'),
    path('logout/', views.logout, name='logout'),
    path('profile_read/<int:id>', views.profile_read2, name='profile_read'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('modify_form/', views.modify_form, name='modify_form'),
    path('profile_modify/', views.profile_modify, name='profile_modify'),
    path('attachPhoto/', views.attachPhoto, name='attachPhoto'),
]
