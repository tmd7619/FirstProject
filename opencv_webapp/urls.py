from django.contrib import admin
from django.urls import path, include
from opencv_webapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('web_ver/', views.web_ver, name='web_ver'),
    path('browser/', views.browser, name='browser'),
    path('mobile/', views.mobile, name='mobile'),
    path('alarm_ajax/', views.alarm_ajax, name='alarm_ajax'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)