from django.urls import path

from django.conf.urls import url
#####    . is to indicate the current directory, 'views.py' file from the current directory
from . import views

app_name = 'app_blog'

urlpatterns  = [
    path('', views.blog_home, name='blog_home'),
    path('create/', views.blog_create, name='blog_create'),
    path('update/<id>/', views.blog_update, name='blog_update'),
    path('delete/<id>/', views.blog_delete, name='blog_delete'),
    path('detail/<id>/', views.blog_detail, name='blog_detail'),

    path('my_blogs/', views.My_blogs.as_view(), name="my_blogs"),
    path('liked/<pk>/', views.liked, name='liked'),
    path('unliked/<pk>/', views.unliked, name='unliked'),
]
