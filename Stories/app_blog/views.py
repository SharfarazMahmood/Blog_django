from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid

##import
from django.views.generic import View, TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView

from app_blog.models import Blog, Comment, Likes
from app_blog.forms import CommentForm

# Create your views here.

class Blog_list (ListView):
    context_object_name = "blogs"
    model = Blog
    template_name = 'app_blog:blog_list.html'
    fields = ('blog_title', 'blog_content', 'blog_image')
    queryset = Blog.objects.order_by('-publish_date')


class Create_blog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'app_blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))


@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm( request.POST )
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect( reverse('app_blog:blog_details', kwargs={'slug':slug} ) )
    dict = {'blog':blog, 'comment_form':comment_form}
    return render(request, 'app_blog/blog_details.html', context=dict)
