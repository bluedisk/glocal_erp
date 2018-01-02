from django.contrib import admin
from django.contrib.admin.decorators import register
from teacher.models import Teacher


@register(Teacher)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth', 'subject1' 'subject2', 'phone', 'created_at']