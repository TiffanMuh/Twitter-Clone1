from django.shortcuts import render
from django.http import HttpResponse
from .forms import PostForm
from .models import Post
from django.forms import forms
from django.http.response import HttpResponseRedirect
from django.forms.fields import ImageField


def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect(form.errors.as_json())

    # Get all posts, limit = 20
    posts = Post.objects.all().order_by('-created_at')[:20]

    # Show
    return render(request, 'posts.html',
                  {'posts': posts})


def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')


def like(request, post_id):
    newlikecount = Post.objects.get(id=post_id)
    newlikecount.likecount += 1
    newlikecount.save()
    return HttpResponseRedirect('/')


def edit(request, post_id):
    posts = Post.objects.get(id=post_id)
    if request.method == "GET":
        posts = Post.objects.get(id=post_id)
        return render(request, "edit.html", {"posts": posts})
    if request.method == "POST":
        posts = Post.objects.get(id=post_id)
        form = PostForm(request.POST, request.FILES, instance=posts)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("not valid")
