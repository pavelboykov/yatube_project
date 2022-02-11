from django.shortcuts import render, get_object_or_404
from .models import Post, Group

VISIBLE_ELEMENTS = 10


def index(request):
    posts = Post.objects.order_by('-pub_date')[:VISIBLE_ELEMENTS]
    title = 'Последние обновления на сайте'
    context = {
        'title': title,
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all().order_by('-pub_date')[:VISIBLE_ELEMENTS]
    title = f'Записи сообщества {group.title}'
    context = {
        'title': title,
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)
