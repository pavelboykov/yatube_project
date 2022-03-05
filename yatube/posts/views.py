from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Post, Group, User
from . forms import PostForm


VISIBLE_ELEMENTS = 10


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, VISIBLE_ELEMENTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all().order_by('-pub_date')
    paginator = Paginator(post_list, VISIBLE_ELEMENTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author).order_by('-pub_date')
    paginator = Paginator(posts, VISIBLE_ELEMENTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_author = Post.objects.filter(author=post.author).order_by('-pub_date')
    context = {
        'post': post,
        'posts_author': posts_author,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = Post(
                text=form.cleaned_data["text"],
                author=request.user,
                group=form.cleaned_data["group"]
            )
            new_post.save()
            return redirect(f'/profile/{request.user}/')
        return render(request, 'posts/create_post.html', {'form': form, })
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form, })


@login_required
def post_edit(request, post_id):
    is_edit = True
    post_to_edit = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post_to_edit)
    context = {
        'form': form,
        'post_to_edit': post_to_edit,
        'is_edit': is_edit,
    }
    if request.user.id != post_to_edit.author_id:
        return redirect('posts:post_detail', post_id=post_id)
    else:
        if form.is_valid():
            post_to_edit = form.save(commit=False)
            post_to_edit.author = request.user
            post_to_edit.save()
            return redirect('posts:post_detail', post_id=post_id)
        return render(request, 'posts/create_post.html', context)
