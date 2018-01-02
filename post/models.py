# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.urlresolvers import reverse


class PostCategory(models.Model):
    
    class Meta:
        verbose_name = "포스트 카테고리"
        verbose_name_plural = "포스트 카테고리 목록"

    def __str__(self):
        return self.name

    code = models.CharField('카테고리 코드', max_length=10, primary_key=True)
    name = models.CharField('카테고리 제목', max_length=40)
    desc = models.CharField('카테고리 한줄 설명', max_length=80)
    
    template = models.CharField('특수 템플릿',
                                max_length=80,
                                default=None,
                                null=True,
                                blank=True,
                                help_text="이 카테고리가 특수한 템플릿을 쓸 경우 템플릿명"
                                )
    

class Post(models.Model):

    class Meta:
        verbose_name = "포스트"
        verbose_name_plural = "포스트 목록"

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("post", args=[self.id])
        
    cate = models.ForeignKey(PostCategory, blank=True, null=True)

    active = models.BooleanField('표시여부', default=True, help_text='체크 되어 있을 때 리스트에 표시 됩니다')

    title = models.CharField('포스트 제목', max_length=40)
    content = RichTextUploadingField('포스트 내용')
    summery = models.TextField('요약 내용')

    updated = models.DateTimeField('업데이트', auto_now=True)
    created = models.DateTimeField('생성일', auto_now_add=True)

