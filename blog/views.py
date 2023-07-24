from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Author
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm
# Create your views here.


def homepage(request):
    posts = Post.objects.all()
    return render(request, 'blog/homepage.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.comment_set.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_form = form.save(commit=False)
            author = Author.objects.get(user=request.user)
            post_form.author = author
            post_form.save()
            return redirect('post_detail', pk=post_form.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

def comment_create(request, post_pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            post = Post.objects.get(pk=post_pk)
            comment_form.post = post
            if request.user.is_authenticated:
                user = request.user.username
                if User.objects.get(username=user).author_set.all().count() >= 1:
                    user = User.objects.get(username=user).author_set.all()[0]
                comment_form.comment_author = user
            comment_form.save()
            return redirect('post_detail', pk=post_pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})