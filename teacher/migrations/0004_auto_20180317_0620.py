# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-16 21:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20180317_0446'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ('name',), 'verbose_name': '과목', 'verbose_name_plural': '과목 목록'},
        ),
        migrations.AlterModelOptions(
            name='subjectcategory',
            options={'ordering': ('name',), 'verbose_name': '과목 분류', 'verbose_name_plural': '과목 분류 목록'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': '선생님', 'verbose_name_plural': '선생님 목록'},
        ),
        migrations.AlterField(
            model_name='subject',
            name='cate',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='teacher.SubjectCategory'),
        ),
    ]
