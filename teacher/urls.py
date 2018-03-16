# -*- coding: utf-8 -*-

from django.conf.urls import url
from teacher import views

urlpatterns = [

    url(r'regist/$', views.regist, name='regist'),
    url(r'^autocomplete/category/$', views.SubjectCategoryAutocomplete.as_view(create_field='name'), name='category-autocomplete'),
    url(r'^autocomplete/subject/$', views.SubjectAutocomplete.as_view(create_field='name'), name='subject-autocomplete'),
]
