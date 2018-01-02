# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20171130_0745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='강사명')),
                ('active', models.CharField(choices=[('active', '활동'), ('inactive', '비활동'), ('etc', '기타')], max_length=10, verbose_name='활동여부')),
                ('work_type', models.CharField(choices=[('direct', '직영'), ('free', '프리랜서')], max_length=10, verbose_name='근무형태')),
                ('subject1', models.CharField(max_length=100, verbose_name='강의과목1')),
                ('subject2', models.CharField(max_length=100, verbose_name='강의과목2')),
                ('course', models.CharField(max_length=100, verbose_name='개설과목')),
                ('weekday', models.CharField(max_length=100, verbose_name='개설요일')),
                ('phone', models.CharField(blank=True, max_length=80, null=True, verbose_name='연락처')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='이메일')),
                ('address', models.CharField(blank=True, max_length=256, null=True, verbose_name='주소')),
                ('schools', models.ManyToManyField(blank=True, to='home.School', verbose_name='개설학교')),
            ],
            options={
                'verbose_name': '강사',
                'verbose_name_plural': '강사 목록',
            },
        ),
    ]
