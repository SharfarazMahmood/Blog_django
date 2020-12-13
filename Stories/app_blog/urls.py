from django.urls import path
#####    . is to indicate the current directory, 'views.py' file from the current directory
from . import views

app_name = 'app_blog'

urlpatterns  = [
    path('', views.Blog_list.as_view(), name='blog_list'),
    path('create_blog/', views.Create_blog.as_view(), name='create_blog'),
    path('blog_details/<slug>/', views.blog_details, name='blog_details'),
    path('my_blogs/', views.My_blogs.as_view(), name="my_blogs"),
    path('edit_blog/<pk>/', views.Edit_blog.as_view(), name="edit_blog"),
    path('liked/<pk>/', views.liked, name='liked'),
    path('unliked/<pk>/', views.unliked, name='unliked'),
]
