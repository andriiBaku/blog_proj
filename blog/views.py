from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.

def homepage(request):
    posts = Post.objects.all()
    return render(request, 'blog/homepage.html', {'posts': posts})