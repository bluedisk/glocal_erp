from django.contrib import admin
from django.contrib.admin.decorators import register
from teacher.models import Teacher


@register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth', 'subject1', 'subject2', 'phone', 'create_at']
    list_filter = ['subject1', 'subject2']
