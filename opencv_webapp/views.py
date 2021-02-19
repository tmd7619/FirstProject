from django.shortcuts import render, redirect
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from django.conf import settings
from .opencv_browser import opencv_browser
from .opencv_moblie import opencv_mobile
from django.http      import JsonResponse
from .models import *
from stuApp.models import StuProfile
import datetime

# Create your views here.
def web_ver(request):
    return render(request, 'web_ver.html')

def browser(request):

    if request.method == 'POST' and request.POST['flag'] == 'Bbtn':
        flag = opencv_browser(1)
        print('browser return value', flag)
        if flag == 1:
            check_day = str(datetime.datetime.today())
            check_hour = int(check_day[11:13])
            check_min = int(check_day[14:16])
            check_sec = int(check_day[17:19])
            user_name = request.session['user_name']
            p = StuProfile.objects.get(user_name=user_name)
            if (check_hour == 8 and 50 <=check_min and check_min <= 59) or (check_hour == 9 and 00<=check_min and check_min < 5):
                list = [{'browser_info': 'QR 출석을 완료했습니다. '}]
                p.user_attend = p.user_attend + 1
            else:
                list = [{'browser_info': 'QR 출석을 완료했습니다. 지각입니다.'}]
                p.user_late = p.user_late + 1
            p.save()
            return JsonResponse(list, safe=False)
        else:
            list = [{'browser_info': 'QR을 찾지 못했습니다. '}]
            return JsonResponse(list, safe=False)
    list = [{'browser_info': 'QR을 찾지 못했습니다. '}]
    return JsonResponse(list, safe=False)

def mobile(request):
    if request.method == 'POST':
        flag = opencv_mobile(1)
        print('mobile return value - ', flag)
        if flag == 1:
            check_day = str(datetime.datetime.today())
            check_hour = int(check_day[11:13])
            check_min = int(check_day[14:16])
            check_sec = int(check_day[17:19])
            user_name = request.session['user_name']
            p = StuProfile.objects.get(user_name=user_name)
            if (check_hour == 8 and 50 <= check_min and check_min <= 59) or (
                    check_hour == 9 and 00 <= check_min and check_min < 5):
                list = [{'mobile_info': 'QR 출석을 완료했습니다. '}]
                p.user_attend = p.user_attend + 1
            else:
                list = [{'mobile_info': 'QR 출석을 완료했습니다. 지각입니다.'}]
                p.user_late = p.user_late + 1
            p.save()
            print('list -', list)
            return JsonResponse(list, safe=False)
        else:
            list = [{'mobile_info': 'QR을 찾지 못했습니다. '}]
            return JsonResponse(list, safe=False)
    else:
        list = [{'mobile_info': 'QR을 찾지 못했습니다. '}]
        return JsonResponse(list, safe=False)

def alarm_ajax(request):
    if request.method == 'POST' and request.POST['flag'] == 'Abtn':
        print(request.POST['flag'])
        p = StuProfile.objects.get(user_name=request.user)
        p.user_absent = p.user_absent + 1
        p.save()
    # print('ajax - param - ', flag)
        list = [{'info': '신호출결이 완료되었습니다. '}]
    else:
        list = [{'info': '다시 시도해주세요 . '}]
    return JsonResponse(list, safe=False)
