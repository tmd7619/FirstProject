from django.shortcuts import render, redirect
import datetime
from .models import *
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from stuApp.models import StuProfile
from django.http import JsonResponse

# Create your views here.
def main(request):
    # today 날짜로 조건 설정해서 표시되는 프로젝트 달라지게
    subject_day = str(datetime.date.today())
    # subject_day = str(datetime.date(2021, 2, 25))    #테스트용 날짜 변경
    ab_date = int((subject_day[5:7]) + (subject_day[8:]))
    if ab_date in range(201, 219):
        subject_name = '세미프로젝트'
        pro_startdate = datetime.datetime(2021, 2, 1, 9, 0, 0, 1  ) #.000001초 단위 만들기 위해 오차 만들기
        pro_enddate = datetime.datetime(2021, 2, 19, 18, 0, 0, 0)
        pro_start = '2021.02.01'
        pro_end = '2021.02.19'
    elif ab_date in range(220, 402 ):
        subject_name = 'AI 활용을 위한 딥러닝'
        pro_startdate = datetime.datetime(2021, 2, 19, 18, 0, 0, 1  ) #.000001초 단위 만들기 위해 오차 만들기
        pro_enddate = datetime.datetime(2021, 4, 2, 18, 0, 0, 0)
        pro_start = '2021.02.20'
        pro_end = '2021.04.02'
    elif ab_date in range(403, 423):
        subject_name = 'AI 프로젝트'
        pro_startdate = datetime.datetime(2021, 4, 2, 18, 0, 0, 1  ) #.000001초 단위 만들기 위해 오차 만들기
        pro_enddate = datetime.datetime(2021, 4, 23, 18, 0, 0, 0)
        pro_start = '2021.04.03'
        pro_end = '2021.04.23'
    else:
        subject_name = '융복합 프로젝트'
        pro_startdate = datetime.datetime(2021, 4, 23, 18, 0, 0, 1  ) #.000001초 단위 만들기 위해 오차 만들기
        pro_enddate = datetime.datetime(2021, 6, 4, 18, 0, 0, 0)
        pro_start = '2021.04.24'
        pro_end = '2021.06.04'


    #종강 날짜
    end_datetime = datetime.datetime(2021, 6, 4, 18, 0, 0, 0)
    # 오늘 날짜
    today_now = datetime.datetime.today()
    # today_now = datetime.datetime(2021, 2, 25, 10, 11, 35, 2) #테스트용 날짜 변경

    #1. 종강
    remain_endclass = end_datetime - today_now
    # 18 days, 8:59:59.999999
    #   1 days, 8:59:59.999999
    class_total_second = remain_endclass.total_seconds()
    class_percentage = 100 - (class_total_second/13683600)*100 #귀찮아서 그냥 100에서 뺌

    # 2. 프로젝트별, 날짜는 위에서 한번에 지정
    pro_prog = today_now - pro_startdate  #과목 시작일부터 오늘까지 경과 시간
    pro_period = pro_enddate - pro_startdate #과목 전체 시간
    pro_prog_total_second = pro_prog.total_seconds()
    pro_period_total_second = pro_period.total_seconds()
    pro_percentage = (pro_prog_total_second/pro_period_total_second)*100

    # 3. 오늘 하루 시간
    # 시간 불러오기
    today_date = datetime.date.today()
    # today_date = datetime.date(2021, 2, 25) #테스트용 날짜 변경
    today_str = str(today_date)
    today = today_str +" "+ '09:00:00.000000'
    today_start = datetime.datetime.strptime(today, '%Y-%m-%d %H:%M:%S.%f')
    #하루 9시간중 경과한 시간 구하기
    total_second = (today_now -today_start).total_seconds()
    today_percentage = (total_second/32400)*100

    context = {'today_per' : today_percentage,
                      'today' : today_date,
                      'class_per' : class_percentage,
                      'pro_per' : pro_percentage,
                      'pro_sec' : pro_period_total_second,
                      'subject_name' : subject_name,
                      'pro_start' : pro_start,
                      'pro_end' : pro_end}

    # 개인 커스텀 그래프
    user_name = request.session['user_name']
    if user_name:
        xyz = StuProfile.objects.get(user_name=user_name) #개인 그래프용 db 호출
        context['custom_name'] = xyz.calendar_name
        context['custom_startdate'] = xyz.calendar_start
        context['custom_enddate'] = xyz.calendar_end
        context['id'] = xyz.user_name
        if xyz.calendar_name == None:
            custom_period = None
            context['custom_seconds'] = 1   #보이지 않는 상태이므로 그냥 1로 초기화
            context['custom_percentage'] = 1
        else:
            custom_period = xyz.calendar_end - xyz.calendar_start
            custom_total_second = custom_period.total_seconds()
            custom_start_str = datetime.datetime.strftime(xyz.calendar_start, '%Y-%m-%d %H:%M:%S')
            custom_start_aware = datetime.datetime.strptime(custom_start_str, '%Y-%m-%d %H:%M:%S')
            if custom_start_aware > today_now:
                custom_today = custom_start_str
            else:
                custom_today = str(today_now)[:-7]
            custom_today2 = datetime.datetime.strptime(custom_today, '%Y-%m-%d %H:%M:%S')
            custom_prog = custom_today2 - custom_start_aware
            custom_prog = custom_prog - datetime.timedelta(hours=9)
            custom_prog_second = custom_prog.total_seconds()
            custom_percentage = (custom_prog_second/custom_total_second)*100
            context['custom_seconds'] = custom_total_second
            context['custom_percentage'] = custom_percentage
    else:
        context['id'] = None
        context['custom_seconds'] = 1
        context['custom_percentage'] = 1

    return render(request, 'main.html', context)

def custom_period(request):
    start_date = request.POST['start_d']
    start_time = request.POST['start_t']
    start = start_date + " " + start_time
    end_datetime = request.POST['end_d']
    end_time = request.POST['end_t']
    end = end_datetime + " " + end_time
    period_name = request.POST['period_name']

    user_name = request.session['user_name']
    data = StuProfile.objects.get(user_name=user_name)
    data.calendar_name = period_name
    data.calendar_start = start
    data.calendar_end = end
    data.save()

    return redirect('atdApp:main')

def custom_del(request):
    user_name = request.session['user_name']
    data = StuProfile.objects.get(user_name=user_name)
    data.calendar_name = ''
    data.save()
    return redirect('atdApp:main')


def ranking(request):
    b = StuProfile.objects.order_by('-user_attend')   #출석순 내림차순 정렬
    c = list(b)
    stu_list = [ ]
    for x in c:
        stu_list.append([x.user_name, x.user_attend, x.user_absent, "", ""])
    # 출석 1등 (복수) 뽑아내기
    most_att = c[0].user_attend
    plural = len(list(StuProfile.objects.filter(user_attend = most_att)))
    if plural == 1:
        first_one = stu_list[0][0]
    elif plural !=1 :
        first_one = str(stu_list[0][0]) + ' 외 ' + str(plural-1) + '명'

    abs = StuProfile.objects.order_by('-user_absent')
    abs_list = list(abs)
    ab_stu_list = []
    for y in abs_list:
        ab_stu_list.append([y.user_name, y.user_attend, y.user_absent, "", ""])
    most_abs = abs_list[0].user_absent
    plural2 = len(list(StuProfile.objects.filter(user_absent = most_abs)))
    if plural2 == 1:
        first_one2 = ab_stu_list[0][0]
    elif plural2 !=1 :
        first_one2 = str(ab_stu_list[0][0]) + ' 외 ' + str(plural2-1) + '명'

    context = { 'tmp_table' : stu_list, 'attend_1' : first_one, 'absent_1' : first_one2}
    context['what'] = '출석'
    context['id'] = request.session['user_name']
    return render(request, 'rank.html', context)


def abrank(request):
    abs = StuProfile.objects.order_by('-user_absent')   #출석순 내림차순 정렬
    abs_list = list(abs)
    stu_list = [ ]
    for x in abs_list:
        stu_list.append([x.user_name, x.user_attend, x.user_absent, "", ""])
    stu_list[0][4] = '1등'
    most_abs = abs_list[0].user_absent
    plural2 = len(list(StuProfile.objects.filter(user_absent = most_abs)))
    if plural2 == 1:
        first_one2 = stu_list[0][0]
    else :
        first_one2 = str(stu_list[0][0]) + ' 외 ' + str(plural2-1) + '명'

    b = StuProfile.objects.order_by('-user_attend')   #출석순 내림차순 정렬
    c = list(b)
    most_att = c[0].user_attend
    plural = len(list(StuProfile.objects.filter(user_attend = most_att)))
    if plural == 1:
        first_one = c[0]
    else :
        first_one = str(c[0]) + ' 외 ' + str(plural-1) + '명'
        
    context = {'tmp_table' : stu_list, 'absent_1' : first_one2, 'attend_1' : first_one}
    context['what'] = '결석'
    return render(request, 'rank.html', context)




def curri(request):
    # 날짜 테스트 
    
    # 진행도 측정 부분 : 모듈로 만들어야 할것 
    today_now = datetime.datetime.today()
    subject_day = str(datetime.date.today())
    ab_date = int((subject_day[5:7]) + (subject_day[8:]))
    if ab_date in range(201, 216):
        subject_name = '세미 프로젝트'
        pro_startdate = datetime.datetime(2021, 2, 1, 9, 0, 0, 1  ) #.000001초 단위 만들기 위해 오차 만들기
        pro_enddate = datetime.datetime(2021, 2, 16, 18, 0, 0, 0)
    elif ab_date in range(217, 219):
        subject_name = '취업특강2'
        pro_startdate = datetime.datetime(2021, 2, 17, 9, 0, 0, 1  ) #.000001초 단위 만들기 위해 오차 만들기
        pro_enddate = datetime.datetime(2021, 2, 19, 18, 0, 0, 0)
    elif ab_date in range(220, 402 ):
        subject_name = 'AI 활용을 위한 딥러닝'
        pro_startdate = datetime.datetime(2021, 2, 20, 9, 0, 0, 1  ) #.000001초 단위 만들기 위해 오차 만들기
        pro_enddate = datetime.datetime(2021, 4, 2, 18, 0, 0, 0)
    elif ab_date in range(403, 423):
        subject_name = 'AI 프로젝트'
        pro_startdate = datetime.datetime(2021, 4, 2, 9, 0, 0, 1  ) #.000001초 단위 만들기 위해 오차 만들기
        pro_enddate = datetime.datetime(2021, 4, 23, 18, 0, 0, 0)
    else:
        subject_name = '융복합 프로젝트'
        pro_startdate = datetime.datetime(2021, 4, 23, 9, 0, 0, 1  ) #.000001초 단위 만들기 위해 오차 만들기
        pro_enddate = datetime.datetime(2021, 6, 4, 18, 0, 0, 0)
    pro_prog = today_now - pro_startdate  #과목 시작일부터 오늘까지 경과 시간
    pro_period = pro_enddate - pro_startdate #과목 전체 시간
    pro_prog_total_second = pro_prog.total_seconds()
    pro_period_total_second = pro_period.total_seconds()
   
    pro_percentage = (pro_prog_total_second/pro_period_total_second)*100
    #진행도 측정 부분 : 모듈로 만들어야 할것

    ojb = TotalCurriculum.objects.get(subject_name=subject_name)
    if pro_percentage >= 100:
        ojb.subject_comp = 100
    else:
        ojb.subject_comp = pro_percentage
    ojb.save()
    rn = datetime.date.today()
    past = TotalCurriculum.objects.filter(subject_date__lte=rn)
    curri_list = TotalCurriculum.objects.order_by('subject_date')

    context = {'list' : curri_list, 'len' : rn}
    return render(request, 'curriculum.html' , context)


def add_attend(request):
    name = request.POST['name']
    person = StudentUser.objects.get(user_name=name)
    person.user_attend = person.user_attend + 1
    person.save()
    context = {}
    context['alert'] = name+'님 출석 확인되었습니다'
    return JsonResponse(context, safe=False)

def text(request):
    return render(request, 'text.html')