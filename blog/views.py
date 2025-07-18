from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from taggit.models import Tag

from .forms import CommentForm
from .models import Post


def post_list(request, tag_slug=None):
    posts_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)

    context = {
        "posts": posts,
        "tag": tag,
    }
    return render(request, "blog/post/list.html", context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "blog/post/detail.html", context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        "post": post,
        "form": form,
        "comment": comment
    }
    return render(request, "blog/post/comment.html", context)
