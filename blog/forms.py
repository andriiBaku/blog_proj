from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'category', 'post_image', 'post_published',)

class PostStatusForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_status',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
