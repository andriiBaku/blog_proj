from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ManyToManyField('Category', blank=True)
    post_created = models.DateTimeField(auto_now_add=True)
    post_published = models.DateTimeField(null=True, blank=True)
    post_image = models.ImageField(upload_to='blog_images/%Y/%m/%d/', blank=True)

    STATUS_CHOICES = (
        ('cd', 'canceled'),
        ('pg', 'processing'),
        ('pd', 'posted'),
    )

    post_status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='i_p')

    def __str__(self):
        return self.title

    def get_author_name(self):
        return str(self.author)

    def get_comments_count(self):
        comments_count = self.comment_set.all().count()
        return comments_count

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return f'Comment №{self.pk}'