# -*- coding: utf-8 -*-

from django.conf.urls import url
from teacher import views

urlpatterns = [

    url(r'regist/$', views.regist, name='regist'),

]
