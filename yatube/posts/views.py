from django.http import HttpResponse


def index(request):
    return HttpResponse('Главная страница социальной сети блогеров')


def group_posts(request, slug):
    return HttpResponse(f'Пост: {slug}')