from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Post, Author, Category, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import TemplateView, UpdateView
from .forms import PostForm, CommentForm, PostStatusForm
from datetime import datetime


# Create your views here.


def homepage(request):
    posts = Post.objects.filter(post_status='pd')
    categories = Category.objects.all()
    return render(request, 'blog/homepage.html', {'posts': posts, 'categories': categories})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.comment_set.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


@permission_required('blog.add_post', login_url='/account/signin/')
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.author = request.user
            post_form.save()
            return redirect('post_detail', pk=post_form.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@permission_required('blog.change_post', login_url='/account/signin/')
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


@permission_required('blog.set_post_status', login_url='/account/signin/')
def update_post_status_view(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostStatusForm(request.POST, instance=post)
        if form.is_valid():
            post_form = form.save(commit=False)
            if form.cleaned_data.get('post_status') == 'pd':
                post.post_published = datetime.now()
                post.save()
            post_form.save()
            return redirect('unpublished_posts')
    else:
        form = PostStatusForm(instance=post)
        return render(request, 'blog/post_form.html', {'form': form})


class GetUnpublishedPosts(LoginRequiredMixin, TemplateView):
    template_name = 'blog/unpublished_posts.html'
    login_url = '/account/signin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['posts'] = Post.objects.all().exclude(post_status='pd')
        return context


class GetCategories(TemplateView):
    template_name = 'blog/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context


class GetPostsByCategory(TemplateView):
    template_name = 'blog/posts_by_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['posts'] = Category.objects.get(pk=self.kwargs.get('pk')).post_set.all()
        context['category_name'] = Category.objects.get(pk=self.kwargs.get('pk')).name
        return context


class GetPostsByUser(LoginRequiredMixin, TemplateView):
    template_name = 'blog/posts_by_user.html'
    login_url = '/account/signin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = User.objects.get(username=self.kwargs.get('username'))
        context['posts'] = Post.objects.filter(author=user)
        return context


@permission_required('blog.add_comment', login_url='/account/signin/')
def comment_create(request, post_pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            post = Post.objects.get(pk=post_pk)
            comment_form.post = post
            user = User.objects.get(username=request.user.username)
            comment_form.comment_author = user
            comment_form.save()
            return redirect('post_detail', pk=post_pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_add_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.like += 1
    comment.save()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_add_dislike(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.dislike += 1
    comment.save()
    return redirect('post_detail', pk=comment.post.pk)
