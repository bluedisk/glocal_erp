# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-16 21:26
from __future__ import unicode_literals

import re

from django.db import migrations
from django.db import transaction


@transaction.atomic
def clean_phone(apps, scheme_editor):
    ex = re.compile(r"^(02|01.|[0-9]{3})[-.\s]*([0-9]+)[-.\*\s]*([0-9]{4})")

    Teacher = apps.get_model('teacher', 'Teacher')
    for teacher in Teacher.objects.all():
        matchs = ex.match(teacher.phone)

        if not matchs:
            raise ValueError("Wrong format ", teacher.phone)

        teacher.phone = "-".join(matchs.groups())
        teacher.save()


@transaction.atomic
def clean_birthday(apps, scheme_editor):
    ex = re.compile(r"^(?:19|10)?([0-9]{2})[\.년\s\-/]*([0-9]{1,2})[\.월\s\-/]*([0-9]{1,2})[일\s\.]*$")

    Teacher = apps.get_model('teacher', 'Teacher')
    for teacher in Teacher.objects.all():
        matchs = ex.match(teacher.birth)
        if not matchs:
            raise ValueError("Wrong format ", teacher.birth)

        teacher.birth = "19%02d/%02d/%02d" % tuple(int(n) for n in matchs.groups())
        teacher.save()


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_auto_20180317_0620'),
    ]

    operations = [
        migrations.RunPython(clean_phone),
        migrations.RunPython(clean_birthday)
    ]
