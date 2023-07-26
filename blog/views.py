from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Post, Author, Category
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from .forms import PostForm, CommentForm


# Create your views here.


def homepage(request):
    posts = Post.objects.filter(post_status='pd')
    categories = Category.objects.all()
    return render(request, 'blog/homepage.html', {'posts': posts, 'categories': categories})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.comment_set.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


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


class UpdatePostStatus(UpdateView):
    model = Post
    fields = ['post_status']
    success_url = reverse_lazy('unpublished_posts')


class GetUnpublishedPosts(LoginRequiredMixin ,TemplateView):
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
