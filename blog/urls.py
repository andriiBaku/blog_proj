from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path('^$', views.homepage, name='homepage'),
    re_path('^posts/unpublished/$', views.GetUnpublishedPosts.as_view(), name='unpublished_posts'),
    re_path('^posts/by_user/(?P<username>\w+)/$', views.GetPostsByUser.as_view(), name='posts_by_username'),
    re_path('^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    re_path('^post/create/$', views.post_create, name='post_create'),
    re_path('^post/(?P<pk>\d+)/update/$', views.post_update, name='post_update'),
    re_path('^post/(?P<pk>\d+)/update_status/$', views.update_post_status_view, name='update_post_status'),
    path('post/<int:post_pk>/comment/create/', views.comment_create, name='comment_create'),
    re_path('^category/all/$', views.GetCategories.as_view(), name='get_categories'),
    re_path('^category/(?P<pk>\d+)/posts/$', views.GetPostsByCategory.as_view(), name='posts_by_category'),
    re_path('^comment/(?P<pk>\d+)/add_like/$', views.comment_add_like, name='add_comment_like'),
    re_path('^comment/(?P<pk>\d+)/add_dislike/$', views.comment_add_dislike, name='add_comment_dislike'),
]
