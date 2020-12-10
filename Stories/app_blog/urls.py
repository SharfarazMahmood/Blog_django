from django.urls import path
#####    . is to indicate the current directory, 'views.py' file from the current directory
from . import views

app_name = 'app_blog'

urlpatterns  = [
    path('', views.blog_list, name='blog_list'),
]
