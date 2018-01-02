from django.db import models


class Teacher(models.Model):

    def __str__(self):
        return "%s - %s" % (self.name, self.birth)

    name = models.CharField("강사명", max_length=30)
    birth = models.CharField("생년월일", max_length=30)

    subject1 = models.CharField("지도 과목 1", max_length=30)
    subject2 = models.CharField("지도 과목 2", max_length=30, null=True, blank=True)

    postcode = models.CharField("우편번호", max_length=10)
    addr1 = models.CharField("주소", max_length=200)
    addr2 = models.CharField('상세주소', max_length=200)

    email = models.EmailField("이메일")
    phone = models.CharField("전화번호", max_length=30)

    portrait = models.ImageField("증명사진", upload_to="portrait")
    document = models.FileField("방과후학교 지도사 신청 서류", upload_to="document", help_text="위에서 양식을 다운로드 해주세요")

    create_at = models.DateField("등록일자", auto_now_add=True)

