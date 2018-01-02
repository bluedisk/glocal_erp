# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from page.models import Page

register = template.Library()


@register.simple_tag(takes_context=True)
def render_page(context, page_code):
    if not page_code:
        raise Http404("Page code is needed to render")

    page, _ = Page.objects.get_or_create(code=page_code, defaults={'title': page_code, 'content': page_code})

    return template.Template(page.content).render(template.Context({
        'user': context['user'],
        'title': page.title,
        'edit': reverse('admin:page_page_change', args=[page.id])
    }))
