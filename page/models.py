# -*- coding: utf-8 -*-
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Page(models.Model):

    class Meta:
        verbose_name = "페이지"
        verbose_name_plural = "페이지 목록"

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return "/%s/" % self.code

    title = models.CharField('페이지 제목', max_length=40)
    subtitle = models.CharField('페이지 부제목(선택)', max_length=100, blank=True, null=True)
    featured = models.ImageField('타이틀 이미지', upload_to='featured', blank=True, null=True)

    THEME_CHOICES = (
        ('', '밝게'),
        ('dark', '어둡게'),
        ('gray', '회색조'),
        ('custom', '커스텀')
    )
    theme = models.CharField('컬러 테마', max_length=10, choices=THEME_CHOICES, default='', blank=True)

    code = models.SlugField('페이지 코드', unique=True)

    content = RichTextUploadingField('페이지 내용', config_name='page')
    style = models.TextField('Style', default='', blank=True, null=True)
    script = models.TextField('Script', default='', blank=True, null=True)

    updated = models.DateTimeField('업데이트', auto_now=True)
    created = models.DateTimeField('생성일', auto_now_add=True)
