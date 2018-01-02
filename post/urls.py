# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^(?P<post_id>\d+)/$', views.post, name='post'),
    url(r'^(?P<cate_id>\w+)/$', views.post_list, name='post_list'),

]
