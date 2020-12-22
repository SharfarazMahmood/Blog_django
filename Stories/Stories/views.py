#### views for the pages not depended on the other apps ########
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect


def index(request):
    return HttpResponseRedirect( reverse( 'app_blog:blog_home' ) )
