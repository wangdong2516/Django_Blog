"""
    用户模块的路由配置
"""

from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'login/$', views.LoginView.as_view()),
    re_path(r'mobile/(?P<mobile>1[3-9]\d{9})/$', views.MobileVerifyView.as_view()),
    re_path(r'username/(?P<username>[a-zA-Z0-9_-]{4,16})/$', views.UserNameVerifyView.as_view()),
    re_path(r'sms_code/$', views.SmsCodeView.as_view()),
    re_path(r'register/$', views.UserRegisterView.as_view()),
    re_path(r'^', views.IndexView.as_view()),
]


