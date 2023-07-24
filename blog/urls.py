from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path('^$', views.homepage, name='homepage'),
    re_path('^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    re_path('^post/create/$', views.post_create, name='post_create'),
    re_path('^post/(?P<pk>\d+)/update/$', views.post_update, name='post_update'),
    path('post/<int:post_pk>/comment/create/', views.comment_create, name='comment_create'),
]