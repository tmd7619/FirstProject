from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required


def classboard (reqeust):
    return render(reqeust, 'classboard2.html')

def list (request):
    # context['id'] = request.session['user_name']
    loginSession = request.session['user_name']
    print('list - ', loginSession)
    boards = Quiz.objects.all()
    print('list request -', type(boards), boards)
    context = {'boards': boards , 'id' : loginSession }
    return render(request, 'list2.html', context)

def postForm (reqeust):
    print ('request postFrom =')
    return render(reqeust, 'post2.html')

def post (request):
    loginSession = request.session['user_name']
    print('post - ', loginSession)
    user = User.objects.get(username=loginSession)
    print('post user -', user.id)
    title = request.POST['title']
    content = request.POST['content']
    explanation = request.POST['explanation']
    answer = request.POST['answer']
    classType = request.POST['classType']
    board = Quiz(title=title, content=content, explanation=explanation,
                 answer=answer, classType=classType , writer=user)
    board.save()
    return redirect('hello_app:list')

def read (request, id):
    board = Quiz.objects.get(id=id)
    board.save
    print('read result 2 - ', board)
    context = {'board' : board }
    context['id'] = request.session['user_name']
    context['writer'] = str(board.writer)
    return render(request, 'read2.html', context)

def modifyFrom (request):
    id = request.POST['id']
    board = Quiz.objects.get(id=id)
    context = {'board': board }
    return render (request, 'modify2.html', context)

def modify (request):
    id = request.POST['id']
    title = request.POST['title']
    content = request.POST['content']
    explanation = request.POST['explanation']
    answer = request.POST['answer']
    print ('request -', title, content, explanation, answer)
    board = Quiz.objects.get(id=id)
    board.title = title
    board.content = content
    board.explanation = explanation
    board.answer = answer
    board.save()
    return redirect('hello_app:list')

def remove (request):
    id = request.POST['id']
    print('request remove -', id)
    Quiz.objects.get(id=id).delete()
    return redirect('hello_app:list')

def answerFrom (request):
    id = request.POST['id']
    board = Quiz.objects.get(id=id)
    context = {'board' : board}
    return render (request, 'answer2.html', context)

def answer (request):
    id = request.POST['id']
    re_answer = request.POST['re_answer']
    print ('request -', re_answer)
    board = Quiz.objects.get(id=id)
    if re_answer == board.answer:
        print ('정답입니다!!', re_answer)
        return redirect('hello_app:list')
    else:
        print('오답 입니다!!', re_answer)
        return HttpResponse('오답 입니다!!')
