# -*- coding: utf-8 -*-
from django import template
from post.models import Post, PostCategory
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def get_posts(category_code):
    return Post.objects.filter(active=True, cate__code=category_code)[:4]


@register.simple_tag
def get_post_category_name(category_code):
    try:
        return PostCategory.objects.get(code=category_code).name
    except:
        return ""


@register.simple_tag
def render_category(category_code):
    cate = get_object_or_404(PostCategory, code=category_code)
    posts = Post.objects.filter(active=True, cate=cate)

    return render_to_string('post/style/' + (cate.template or 'basic_list.html'), {
        'cate': cate,
        'posts': posts,
    })

