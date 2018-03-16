from django.contrib import admin
from django.contrib.admin.decorators import register
from django import forms
from teacher.models import Teacher, Subject, SubjectCategory
from dal import autocomplete


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

    list_display = ['name', 'birth', 'subjects_desc',  'phone', 'create_at']
    list_filter = ['subjects__cate']

    list_per_page = 16

    search_fields = ['name', 'birth', 'phone', 'subjects__name']


@register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'cate']
    list_editable = ['name', 'cate']

    list_display_links = None

    search_fields = ['name']
    list_filter = ['cate']


@register(SubjectCategory)
class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    list_editable = ['name', ]

    list_display_links = None

    search_fields = ['name']
