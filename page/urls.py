# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = "page"

urlpatterns = [

    url(r'^(?P<page_id>\d+)/$', views.page, name='page_by_id'),
    url(r'^(?P<page_code>[\w-]+)/$', views.page, name='page_by_code'),
    url(r'^$', views.page, {'page_code': 'home'}, name='home'),
]
