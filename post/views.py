from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse

from post.models import Post, PostCategory


def post(request, post_id):
    if not post_id:
        raise Http404("Page does not exist")

    try:
        content = Post.objects.get(pk=post_id)
    except:
        content = Post.objects.all().order_by('-created')[0]

    return render(request, 'post/post.html', {
        'title': content.title,
        'content': content.content,
        'cate': content.cate,
        'edit': reverse('admin:page_page_change', args=[content.id])
        })


def post_list(request, cate_id):
    cate = get_object_or_404(PostCategory, code=cate_id)
    posts = Post.objects.filter(active=True, cate=cate)

    default_selected = 0
    if posts:
        default_selected = posts[0].id

    selected = int(request.GET.get('id', default_selected))

    return render(request, 'post/list.html', {
        'style_name': 'post/style/' + (cate.template or 'basic_list.html'),
        'cate': cate,
        'posts': posts,
        'selected': selected,
    })
