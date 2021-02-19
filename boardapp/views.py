from django.db.models import Q,Count
from django.shortcuts import render, get_object_or_404, redirect,resolve_url
from django.utils import timezone
from .models import *
from .forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.


def index(request): # 질문 목록 출력
    page = request.GET.get('page', '1') # 입력 파라미터
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준
    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')
    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'question_list.html', context)

def detail(request, question_id): # 내용출력
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'question_detail2.html', context)


def question_create(request): # 질문등록   완성
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            userSession = request.session['user_name']
            user = User.objects.get(username=userSession)
            question.author = user
            question.create_date = timezone.now()
            question.save()
            return redirect('boardapp:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'question_form2.html', context)


def question_modify(request, question_id): # 질문 수정   # 완성
    question = get_object_or_404(Question, pk=question_id)
    userSession = request.session['user_name']
    user = User.objects.get(username=userSession)
    if user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('boardapp:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            userSession = request.session['user_name']
            user = User.objects.get(username=userSession)
            question.author = user
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('boardapp:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'question_form2.html', context)


def question_delete(request, question_id): # 질문삭제 완성
    question = get_object_or_404(Question, pk=question_id)
    userSession = request.session['user_name']
    user = User.objects.get(username=userSession)
    if user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('boardapp:detail', question_id=question.id)
    question.delete()
    return redirect('boardapp:index')


def answer_create(request, question_id): # 답변등록 완성
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            userSession = request.session['user_name']
            user = User.objects.get(username=userSession)
            answer.author = user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('boardapp:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'question_detail2.html', context)


def answer_modify(request, answer_id): # 답변수정 완성
    answer = get_object_or_404(Answer, pk=answer_id)
    userSession = request.session['user_name']
    user = User.objects.get(username=userSession)

    if user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('boardapp:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            userSession = request.session['user_name']
            user = User.objects.get(username=userSession)
            answer.author = user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('boardapp:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'answer_form2.html', context)


def answer_delete(request, answer_id): # 답변삭제 완성
    answer = get_object_or_404(Answer, pk=answer_id)
    userSession = request.session['user_name']
    user = User.objects.get(username=userSession)
    if user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('boardapp:detail', question_id=answer.question.id)


def comment_create_question(request, question_id): # 질문 댓글 등록 완성
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            userSession = request.session['user_name']
            user = User.objects.get(username=userSession)
            comment.author = user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('boardapp:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'comment_form2.html', context)


def comment_modify_question(request, comment_id): # 질문댓글수정
    comment = get_object_or_404(Comment, pk=comment_id)
    userSession = request.session['user_name']
    user = User.objects.get(username=userSession)
    if user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('boardapp:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            userSession = request.session['user_name']
            user = User.objects.get(username=userSession)
            comment.author = user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('boardapp:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'comment_form2.html', context)

def comment_delete_question(request, comment_id): # 댓글 삭제 완성
    comment = get_object_or_404(Comment, pk=comment_id)
    userSession = request.session['user_name']
    user = User.objects.get(username=userSession)
    if user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('board:detail', question_id=comment.question_id)
    else:
        comment.delete()
    return redirect('board:detail', question_id=comment.question_id)


def comment_create_answer(request, answer_id): #답글 댓글등록 완성
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            userSession = request.session['user_name']
            user = User.objects.get(username=userSession)
            comment.author = user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('boardapp:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'comment_form2.html', context)


def comment_modify_answer(request, comment_id): #답글 댓글수정 완성
    comment = get_object_or_404(Comment, pk=comment_id)
    userSession = request.session['user_name']
    user = User.objects.get(username=userSession)
    if user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('boardapp:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            userSession = request.session['user_name']
            user = User.objects.get(username=userSession)
            comment.author = user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('boardapp:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'comment_form2.html', context)


def comment_delete_answer(request, comment_id): #답글 댓글삭제 완성
    comment = get_object_or_404(Comment, pk=comment_id)
    userSession = request.session['user_name']
    user = User.objects.get(username=userSession)
    if user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('boardapp:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('boardapp:detail', question_id=comment.answer.question.id)

def vote_question(request, question_id): # 질문추천등록
    question = get_object_or_404(Question, pk=question_id)
    userSession = request.session['user_name']
    user = User.objects.get(username=userSession)
    if user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(user)
    return redirect('boardapp:detail', question_id=question.id)

def vote_answer(request, answer_id): #답변 추천등록
    answer = get_object_or_404(Answer, pk=answer_id)
    userSession = request.session['user_name']
    user = User.objects.get(username=userSession)
    if user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(user)
    return redirect('boardapp:detail', question_id=answer.question.id)


'''
order_by 함수는 조회한 데이터를 특정 속성으로 정렬하며, 
'-create_date'는 - 기호가 앞에 붙어 있으므로 작성일시의
 역순을 의미한다.
render 함수는 context에 있는 Question 모델 데이터 question_list를 
boardapp/question_list.html 파일에 적용하여 HTML 코드로 변환한다. 
그리고 장고에서는 이런 파일(boardapp/question_list.html)을 템플릿이라 부른다. 
템플릿은 장고의 태그를 추가로 사용할 수 있는 HTML 파일이라 생각하면 된다. 
템플릿에 대해서는 바로 다음 실습 과정을 통해 자연스럽게 알아보겠다.
'''

