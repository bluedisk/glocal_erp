from django.db import models


class Teacher(models.Model):
    class Meta:
        verbose_name = '선생님'
        verbose_name_plural = '선생님 목록'

        ordering = ('name', )

    def __str__(self):
        return "%s - %s" % (self.name, self.birth)

    def subjects_summary(self):
        return ", ".join([s.name for s in self.subjects.all()])

    def address_summary(self):
        return "우:%s %s %s" % (self.postcode, self.addr1, self.addr2)

    subjects_summary.short_description = '과목 목록'

    name = models.CharField("강사명", max_length=30)
    birth = models.CharField("생년월일", max_length=30)

    subjects = models.ManyToManyField("Subject", verbose_name='담당과목')

    postcode = models.CharField("우편번호", max_length=10)
    addr1 = models.CharField("주소", max_length=200)
    addr2 = models.CharField('상세주소', max_length=200)

    email = models.EmailField("이메일")
    phone = models.CharField("전화번호", max_length=30)

    portrait = models.ImageField("증명사진", upload_to="portrait")
    document = models.FileField("방과후학교 지도사 신청 서류", upload_to="document", help_text="위에서 양식을 다운로드 해주세요")

    create_at = models.DateField("등록일자", auto_now_add=True)


class Subject(models.Model):
    class Meta:
        verbose_name = '과목'
        verbose_name_plural = '과목 목록'

        ordering = ('name',)

    def __str__(self):
        return self.name

    name = models.CharField("수업명", max_length=30)
    cate = models.ForeignKey("SubjectCategory")

    def save(self,  *args, **kwargs):
        try:
            self.cate
        except:
            self.cate = SubjectCategory.objects.get(name='미분류')

        super().save(*args, **kwargs)


class SubjectCategory(models.Model):
    class Meta:
        verbose_name = '과목 분류'
        verbose_name_plural = '과목 분류 목록'

        ordering = ('name',)

    def __str__(self):
        return self.name

    name = models.CharField("수업분야", max_length=30)
