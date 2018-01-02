# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Template, RequestContext
from django.http import Http404
from django.core.urlresolvers import reverse
from page.models import Page

from django.core.exceptions import ObjectDoesNotExist


def page(request, page_id=None, page_code=None):

    if not page_id and not page_code:
        raise Http404("Page does not exist")

    page = None

    try:
        if page_id:
            page = Page.objects.get(pk=page_id)

        if page_code:
            page = Page.objects.get(code=page_code)

    except ObjectDoesNotExist:
        raise Http404("Page does not exist")

    if not page:
        raise Http404("Page does not exist")

    content = page.content
    template = 'page/page.html'

    content = Template(content).render(RequestContext(request, {
        'title': page.title,
        'edit': reverse('admin:page_page_change', args=[page.id])
    }))

    return render(request, template, {
        'page': page,
        'content': content,
        'edit': reverse('admin:page_page_change', args=[page.id])
        })

