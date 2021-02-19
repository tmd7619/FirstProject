from django.contrib import admin
from django.urls import path, include
from attendApp import views
from opencv_webapp import views as qr_views
from django.conf import settings
from django.conf.urls.static import static

app_name= 'atdApp'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('ranking/', views.ranking, name='ranking'),
    path('curriculum/', views.curri, name='curri'),
    path('abrank/', views.abrank, name='difrank'),
    path('cusave/', views.custom_period, name='custom_save'),
    path('cudel/', views.custom_del, name='custom_del'),
    path('add/', views.add_attend, name='add'),
    path('text/', views.text, name='text'),
    path('web_ver/', qr_views.web_ver, name='web_ver'),
    path('browser/', qr_views.browser, name='browser'),
    path('mobile/', qr_views.mobile, name='mobile'),
    path('alarm_ajax/', qr_views.alarm_ajax, name='alarm_ajax'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
