# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-16 19:46
from __future__ import unicode_literals

from django.db import migrations
from django.db import transaction

import re


@transaction.atomic
def data_migration(apps, schema_editor):

    category_list = {
        "미분류": {"사이언스블럭", "블록과학", "로보과학", "3D프린팅펜", "전래놀이"},
        "기타": {"돌봄교실", "동화구연"},
        "역사": {"한국사", "세계사", '역사', '창의역사'},
        "한자": {"한자", "한자급수", "한자급수부"},
        "수학": {"교과수학", "멘사수학게임", "수학", "교과수학", "창의수학", "주산암산", "주산과암산", "주산", "수리셈주산"},
        "공예": {"클레이아트", "토탈공예", "공예", "종이접기", "종이접기클레이", "클레이종이접기", "캘리그라피", "에쁜손글씨",
               "POP",  "생활공예", "클레이", "통합공예"},
        "과학": {"과학", "과학(생명", "실험)", "과학실험", "융합과학", "실험과학", "생명과학", "창의과학",
               "항공과학", "항공우주", "우주항공"},
        "로봇": {"로봇과학", "레고", "로봇과학", "레고과학", "케이넥스"},
        "마술": {"교육마술", "마술", "창의마술"},
        "음악": {"사물놀이", "가야금", "민요", "난타", "플룻", "플루트", "바이올린", "통기타", "밴드", "우쿨렐레", "오카리나",
               "보컬트레이닝", "스쿨밴드지도", "리코드", "첼로", '드럼', "리코더", "국악 가야금", "국악 민요"},
        "체육": {"농구", "배드민턴", "축구", "음악줄넘기", "줄넘기", "탁구", "피구", "방송댄스", "에어로빅댄스", "축구", "티볼"},
        "요리": {"아동요리", "창의요리", "요리교실", "요리"},
        "코딩": {"컴퓨터", "코딩", "코딩 ( 스크래치 )", "드론", "코딩", "피지컬코딩"},
        "바둑": {"바둑", "체스"},
        "멘사두뇌게임": {"멘사두뇌게임", "멘사두뇌보드게임", "멘사보드게임", "창의보드", "교육보드", "큐브교실"},
        "미술": {"미술", "밥로스유화(미술)", "서예", "미술회화", "통합미술", "미술심리치료"},
        "논술": {"독서논술", "역사논술", "한우리 독서논술 1학년", "한우리독서논술", "독서논술", "역사논술", "한우리 독서논술 3학년"},
        "외국어": {"영어", "중국어", "일본어", "영어회화"},
        "건축": {"건축교실", "어린이건축", "어린이건축교실"},
        "드론": {"항공드론", "드론", "항공과학", "드론항공"}
    }

    category_dict = {}

    for key, subjects in category_list.items():
        for subject in subjects:
            category_dict[subject] = key

    Teacher = apps.get_model('teacher', 'Teacher')
    Subject = apps.get_model('teacher', 'Subject')
    SubjectCategory = apps.get_model('teacher', 'SubjectCategory')

    category_objs = {}
    for cate in category_list.keys():
        obj = SubjectCategory(name=cate)
        obj.save()
        category_objs[cate] = obj

    subject_objs = {}
    for subject, cate in category_dict.items():
        obj = Subject(name=subject, cate=category_objs[cate])
        obj.save()
        subject_objs[subject] = obj

    ex = re.compile(r"[&./,]")

    for teacher in Teacher.objects.all():
        subject1 = ex.split(teacher.subject1 or "")
        subject2 = ex.split(teacher.subject2 or "")

        for subject in [s.strip() for s in subject1 + subject2]:
            if subject not in category_list:
                raise ValueError("unknown subject ", subject)

            if subject in ('', '-'):
                continue

            teacher.subjects.add(subject_objs[subject])

        teacher.save()


class Migration(migrations.Migration):
    dependencies = [
        ('teacher', '0002_auto_20180317_0444'),
    ]

    operations = [
        migrations.RunPython(data_migration)
    ]

