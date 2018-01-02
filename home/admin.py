from django.contrib import admin
from django.contrib.admin.decorators import register

from home.models import Slide, School, SchoolDocuments, SchoolCategory, Teacher

from adminsortable.admin import SortableAdmin

from dal import autocomplete
from django import forms

admin.site.site_title = "글로컬드림아카데미"
admin.site.site_header = "글로컬드림아카데미 관리자"


@register(Slide)
class SlideAdmin(SortableAdmin):
    pass


class DocumentInline(admin.StackedInline):
    model = SchoolDocuments


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ('__all__')
        widgets = {
            'cate': autocomplete.ModelSelect2Multiple(url='school-category-autocomplete')
        }


@register(School)
class SchoolAdmin(admin.ModelAdmin):
    form = SchoolForm
    inlines = [DocumentInline]

    list_display = ['name', 'cate_list', 'class_type', 'address', 'phone', 'note']


@register(SchoolCategory)
class SchoolCategoryAdmin(admin.ModelAdmin):
    pass


@register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['active', 'name', 'work_type', 'subject1', 'subject2', 'school_list',
                    'course', 'weekday_text', 'phone', 'email', 'address']
    filter_horizontal = ['schools']
