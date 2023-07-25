from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    re_path('^signup/$', views.sign_up, name='sign_up'),
    re_path('^signin/$', views.SignInView.as_view(), name='sign_in'),
    re_path('^logout/$', LogoutView.as_view(next_page='homepage'), name='logout'),
]