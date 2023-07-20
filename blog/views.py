from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Author
from .forms import PostForm
# Create your views here.


def homepage(request):
    posts = Post.objects.all()
    return render(request, 'blog/homepage.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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
    return render(request, 'blog/post_create_form.html', {'form': form})