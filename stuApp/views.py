from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
import csv
import json
from django.views import View
import os
from uuid import uuid4
from django.utils import timezone
from django.contrib.sites.models import *

# Create your views here.

# <a href="{% url 'profile_list' %}">프로필 보기</a>
# urls.py
# def profile_list():
#   DB
#   context = {'key': value}
#   return render('xxxxx.html' , context)
# xxxx.html -> {{xxxx.id}}

def index(request) :
    if request.session.get('user_name') :
        context={'id': request.session['user_name']
                 }
        return render(request, 'rank.html', context)
    else :
        return render(request, 'page-login2.html')

def registerForm2(request) :
    return render(request, 'page-register2.html')

def register(request) :
    if request.method == 'POST':
        name = request.POST['id']
        pwd = request.POST['pwd']
        email = request.POST['email']
        value_bio = request.POST['bio']
        value_contact= request.POST['contact']
        value_location= request.POST['location']

        register111 = User(username=name, password=pwd, email=email)
        register111.save()

        # value_profile_img= request.FILES['profile_img']
        # if 'profile_img' in request.FILES:
        #     file = request.FILES['profile_img']
        #     file_name = file._name
        #     print('register img - ', file_name)
        #     fp = open('%s%s' % ('stuApp/static/images/', file_name), 'wb')
        #     for chunk in file.chunks():
        #         fp.write(chunk)
        #     fp.close()
        # else:
        #     file_name = 'default.png'
        # print('이미지 들어오나 확인...', request.FILES)

        re = StuProfile.objects.get(user_name=name)
        re.bio = value_bio
        re.contact= value_contact
        re.location= value_location
        # re.profile_img=value_profile_img
        # print('이미지 저장 확인', re.profile_img)
        re.save()

    return render(request, 'page-login2.html')

def logout(request) :
    request.session['user_name'] = {}
    request.session.modified= True
    return redirect('stuApp:index')

def loginForm(request) :
    request.session['user_name'] = None

    return render(request, 'page-login2.html')

def login(request) :
    if request.method== 'GET' :
        return redirect('stuApp:index')

    elif request.method=='POST' :
        id = request.POST['id']
        pwd= request.POST['pwd']
        a = User.objects.filter()
        b = []

        for x in a:
            b.append(x.username)

        if id in b:
            user=User.objects.get(username= id, password=pwd)
        else:
            user = None
        context= {}
        if user is not None:
            request.session['user_name'] = user.username

            context['id'] = request.session['user_name']

            print('로그인 시 세션 정보 뭐뭐 넘어가나. 확인-', context)
            # return render (request, 'home2.html', context)
            # return render (request, 'rank.html', context)
            return redirect('atdApp:ranking')

        else :
            return redirect('stuApp:index')

#-----------------------------------------------------------

def profile_list(request) :
    readusers= StuProfile.objects.all()

    context={'readusers' : readusers,
             'id' : request.session['user_name']}
    print('request - ' , readusers)

    return render(request, 'listtest.html', context)

#------------------------------------------------------------
def profile_read2(request, id) :
    read_stu= StuProfile.objects.get(id=id)
    print('아이디체크', id)

    read_user= User.objects.get(username=read_stu.user_name)
    context = {'readpro': read_user,
               'readpro2' : read_stu,
               'id' : request.session['user_name']
               }
    print('확인...', context)
    return render(request, 'readcontest.html', context)
#-------------------------------------------------------

def modify_form(request) :
    id= request.POST['id']
    print('수정 폼에서 받아오는 id는?', id)

    read_one= StuProfile.objects.get(id=id)
    read_two= User.objects.get(username=read_one.user_name)

    context= {'readmodi' : read_two,
              'readmodi2' : read_one,
              'id' : request.session['user_name']
              }

    print('컨텍스트 확인-', context)

    return render(request, 'profile_modifytest.html', context)

# ㄻㄴㅇㄹㅇㄹ
#---------------------------------------------------------
def profile_modify(request) :

    id= request.POST['id']

    bio= request.POST['mybio2']
    contact=request.POST['contact']
    location=request.POST['location']

    print('수정 중 값 확인...', id, bio, contact, location)

    readmodi= StuProfile.objects.get(id=id)

    readmodi.bio= bio
    readmodi.contact=contact
    readmodi.location=location

    readmodi.save()

    return redirect('stuApp:profile_list')

#------------------------------------------
def attachPhoto(request) :
    profile_photo= request.FILES['profile_photo']

    if not profile_photo.name.endswith('.png') and ('jpg') :
        return redirect('index')
