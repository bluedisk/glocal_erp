from zipfile import ZipFile

import os
from django.contrib import admin, messages
from django.contrib.admin.decorators import register
from django import forms
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from io import BytesIO

from teacher.models import Teacher, Subject, SubjectCategory
from dal import autocomplete

from openpyxl import Workbook


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('__all__')

        widgets = {
            'subjects': autocomplete.ModelSelect2Multiple(url='subject-autocomplete')
        }


@register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = SubjectForm

    list_display = ['name', 'birth', 'subjects_summary',  'phone', 'create_at']
    list_filter = ['subjects__cate', 'subjects']

    list_per_page = 16

    search_fields = ['name', 'birth', 'phone', 'subjects__name']
    actions = ['download_xlsx', 'export_attachments']

    def download_xlsx(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        ws.append(['과목명', '생년월일', '연락처', '이메일', '담당과목', '주소', '등록일자'])

        for teacher in queryset:
            ws.append([
                teacher.name,
                teacher.birth,
                teacher.phone,
                teacher.email,
                teacher.subjects_summary(),
                teacher.address_summary(),
                teacher.create_at
            ])

        # dump data to xlsx
        output = BytesIO()
        wb.save(output)

        # make zipped file
        q = request.GET.get('q', None)
        c = request.GET.get('subjects__cate__id__exact', None)
        if c:
            c = SubjectCategory.objects.get(pk=c)

        postfix = ""
        if q:
            postfix = "(%s)" % q.replace(" ", "_")

        if c:
            postfix += "_%s" % c.name

        compressed = BytesIO()
        now = timezone.now()

        filename = 'teachers%s_%s명_%s' % (postfix, queryset.count(), now.strftime("%Y%m%d"))

        with ZipFile(compressed, 'w') as zf:
            zf.writestr(filename + ".xlsx", output.getvalue())

        # make response
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="teacher_%s.zip"' % now.strftime("%Y%m%d")
        response.write(compressed.getvalue())

        return response

    download_xlsx.short_description = u'선택한 선생님 정보 엑셀(xlsx)로 다운받기'

    def add_attachment(self, zipfile, fileobj, filename):
        try:
            fileobj.open()
            data = fileobj.read()
            fileobj.close()

            _, ext = os.path.splitext(os.path.basename(fileobj.name))
            zipfile.writestr("%s%s" % (filename, ext), data)

        except FileNotFoundError:
            pass

    def export_attachments(self, request, queryset):

        now = timezone.now()

        compressed = BytesIO()
        with ZipFile(compressed, 'w') as zf:
            for teacher in queryset.all():
                if teacher.portrait:
                    self.add_attachment(zf, teacher.portrait, '%s_증명사진' % teacher.name)

                if teacher.document:
                    self.add_attachment(zf, teacher.document, '%s_신청서류' % teacher.name)

        # make response
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="attachments_%s.zip"' % now.strftime("%Y%m%d")

        response.write(compressed.getvalue())
        return response

    export_attachments.short_description = "선택된 선생님들 첨부파일 다운받기"


class MergeForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'cate', ]

    do_action = forms.BooleanField(initial=True, widget=forms.HiddenInput())
    action = forms.CharField(initial='merge_action', widget=forms.HiddenInput())


@transaction.atomic
@register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'cate']
    list_editable = ['name', 'cate']

    list_display_links = None

    search_fields = ['name']
    list_filter = ['cate']

    actions = ['merge_action']

    def merge_action(self, request, queryset):
        if 'do_action' in request.POST:
            form = MergeForm(request.POST)
            if form.is_valid():
                subject = form.save()

                teachers = Teacher.objects.filter(subjects__in=queryset)
                for teacher in teachers:
                    teacher.subjects.add(subject)

                queryset.delete()
                messages.success(request, '{0}명의 선생님 정보가 업데이트 되었습니다.'.format(teachers.count()))
                return
        else:
            temp_name = "/".join([s.name for s in queryset.all()])
            first_cate = queryset.all()[0].cate

            form = MergeForm(initial={'name': temp_name, 'cate': first_cate})

        return render(request, 'admin/teacher/merge_subject.html',
                      {'objects': queryset,
                       'opts': Subject._meta,
                       'form': form})

    merge_action.short_description = u'선택한 수업 합치기'


@register(SubjectCategory)
class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    list_editable = ['name', ]

    list_display_links = None

    search_fields = ['name']
