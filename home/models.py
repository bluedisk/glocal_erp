from django.db import models
from adminsortable.models import SortableMixin
from easy_thumbnails.fields import ThumbnailerImageField
from multiselectfield import MultiSelectField
from django.utils.safestring import mark_safe


class Slide(SortableMixin):
    class Meta:
        verbose_name = '슬라이드'
        verbose_name_plural = '슬라이드 목록'
        ordering = ['order']

    title = models.CharField('제목', max_length=30)
    subtitle = models.CharField('부제', max_length=200, null=True, blank=True)

    button_name = models.CharField('버튼명', max_length=30, null=True, blank=True)
    button_link = models.URLField('버튼링크', null=True, blank=True)

    order = models.PositiveSmallIntegerField(default=0, editable=False, db_index=True)

    image = ThumbnailerImageField('image', upload_to='slide', null=True, blank=True)

    def __str__(self):
        return self.title


class SchoolCategory(models.Model):
    class Meta:
        verbose_name = '학교분류'
        verbose_name_plural = '학교분류 목록'

    name = models.CharField('분류명', max_length=50)

    def __str__(self):
        return self.name


class SchoolDocuments(models.Model):
    class Meta:
        verbose_name = '학교문서'
        verbose_name_plural = '학교문서 목록'

    school = models.ForeignKey("School", verbose_name='해당학교')
    name = models.CharField('문서명', max_length=50)
    file = models.FileField('문서', upload_to='school_documents')

    def __str__(self):
        return self.name


class School(models.Model):
    class Meta:
        verbose_name = '학교'
        verbose_name_plural = '학교 목록'

    name = models.CharField('학교명', max_length=50)
    cate = models.ManyToManyField(SchoolCategory, verbose_name='분류')

    CLASS_TYPE_CHOICES = (
        ('direct', '직영'),
        ('outsourcing', '위탁')
    )
    class_type = models.CharField('강좌종류', max_length=20, choices=CLASS_TYPE_CHOICES)

    # 부수정보
    principal = models.CharField('교장명', max_length=80, blank=True, null=True)
    assistant = models.CharField('교감명', max_length=80, blank=True, null=True)

    after_manager = models.CharField('방과후부장', max_length=80, blank=True, null=True)
    school_manager = models.CharField('메니저', max_length=80, blank=True, null=True)

    note = models.TextField('메모', blank=True, null=True)
    # 메모

    address = models.CharField('주소', max_length=256, blank=True, null=True)
    phone = models.CharField('전화번호', max_length=80, blank=True, null=True)

    students = models.IntegerField('전교생수', default=0)

    def __str__(self):
        return self.name

    def cate_list(self):
        return ", ".join([c.name for c in self.cate.all()])

    cate_list.short_description = '분류'


class Teacher(models.Model):
    class Meta:
        verbose_name = '강사'
        verbose_name_plural = '강사 목록'

    # 운영여부 강사명 분류 강의과목 개설학교 개설과목 개설요일 연락처 이메일 주소

    ACTIVE_CHOICES = (
        ('active', '활동'),
        ('inactive', '비활동'),
        ('etc', '기타')
    )

    name = models.CharField('강사명', max_length=80)
    active = models.CharField('활동여부', max_length=10, choices=ACTIVE_CHOICES)

    WORKTYPE_CHOICES = (
        ('direct', '직영'),
        ('free', '프리랜서')
    )
    work_type = models.CharField('근무형태', max_length=10, choices=WORKTYPE_CHOICES)

    subject1 = models.CharField('강의과목1', max_length=100)
    subject2 = models.CharField('강의과목2', max_length=100)

    schools = models.ManyToManyField('School', verbose_name='개설학교', blank=True)

    course = models.CharField('개설과목', max_length=100)

    WEEKDAY_CHOICES = (
        (0, '월'),
        (1, '화'),
        (2, '수'),
        (3, '목'),
        (4, '금'),
        (5, '토'),
        (6, '일')
    )
    weekday = MultiSelectField('개설요일', max_length=14, choices=WEEKDAY_CHOICES)

    phone = models.CharField('연락처', max_length=80, blank=True, null=True)
    email = models.EmailField('이메일', blank=True, null=True)
    address = models.CharField('주소', max_length=256, blank=True, null=True)

    def school_list(self):
        return ", ".join([s.name for s in self.schools.all()])

    school_list.short_description = '개설학교'

    def weekday_text(self):
        days = []
        for idx, val in self.WEEKDAY_CHOICES:
            if str(idx) in list(self.weekday):
                days.append("O")
            else:
                days.append("&nbsp;&nbsp;")

        return mark_safe("&nbsp;"+"".join(days))

    weekday_text.short_description = mark_safe('개설요일<br/>월화수목금토일')
