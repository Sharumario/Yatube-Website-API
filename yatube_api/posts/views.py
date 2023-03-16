from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow


QUANTITY_POSTS = 10


def page_paginator(request, posts):
    return (Paginator(posts, QUANTITY_POSTS)).get_page(request.GET.get('page'))


def index(request):
    return render(
        request,
        'posts/index.html',
        {'page_obj': page_paginator(request,
                                    Post.objects.select_related('author').all()
                                    ),
         }
    )


def group_posts(request, slug):
    groups = get_object_or_404(Group, slug=slug)
    return render(
        request,
        'posts/group_list.html',
        {'group': groups,
         'page_obj': page_paginator(request, groups.posts.all()),
         }
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = request.user.is_authenticated and request.user != author and (
        Follow.objects.filter(user=request.user, author=author))
    return render(
        request,
        'posts/profile.html',
        {'author': author,
         'page_obj': page_paginator(request, author.posts.all()),
         'following': following,
         }
    )


def post_detail(request, post_id):
    return render(
        request,
        'posts/post_detail.html',
        {'post': get_object_or_404(Post, pk=post_id),
         'form': CommentForm(),
         }
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {'form': form
             }
        )
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect(
        'posts:profile',
        request.user
    )


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect(
            'posts:post_detail',
            post_id
        )

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        post = form.save()
        return redirect(
            'posts:post_detail',
            post_id
        )

    return render(
        request,
        'posts/create_post.html',
        {'form': form,
         'is_edit': True
         }
    )


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    return render(
        request, 'posts/follow.html',
        {'page_obj': page_paginator(
            request,
            Post.objects.filter(author__following__user=request.user))
         }
    )


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    is_follower = Follow.objects.filter(user=user, author=author)
    if user != author and not is_follower.exists():
        Follow.objects.create(user=user, author=author)
    return redirect(reverse('posts:profile', args=(username,)))


@login_required
def profile_unfollow(request, username):
    get_object_or_404(
        Follow,
        user=request.user,
        author__username=username
    ).delete()
    return redirect('posts:profile', username=username)
