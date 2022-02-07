from django.http import HttpResponse


def index(request):
    return HttpResponse('Главная страница социальной сети блогеров')


def groups_detail(request, slug):
    return HttpResponse(f'Пост: {slug}')