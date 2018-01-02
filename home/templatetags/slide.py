from django import template
from home.models import Slide

register = template.Library()


@register.simple_tag
def load_slide():
    return Slide.objects.all()
