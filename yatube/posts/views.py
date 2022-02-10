from django.shortcuts import render, get_object_or_404
from .models import Post, Group

visible_elements = 10


def index(request):
    posts = Post.objects.order_by('-pub_date')[:visible_elements]
    title = 'Последние обновления на сайте'
    context = {
        'title': title,
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all().order_by('-pub_date')[:visible_elements]
    title = f'Записи сообщества {str(group)}'
    context = {
        'title': title,
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)
