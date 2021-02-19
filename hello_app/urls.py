from django.contrib import admin
from django.urls import path, include
from hello_app import views

app_name = 'hello_app'

urlpatterns = [
    path('classboard/', views.classboard, name='classboard'),
    path('list/', views.list, name='list'),
    path('postForm/', views.postForm, name='postForm'),
    path('post/', views.post, name='post'),
    path('read/<int:id>', views.read, name='read'),
    path('modifyFrom/', views.modifyFrom, name='modifyFrom'),
    path('modify/', views.modify, name='modify'),
    path('remove/', views.remove, name='remove'),
    path('answerFrom/', views.answerFrom, name='answerFrom'),
    path('answer/', views.answer, name='answer'),
]