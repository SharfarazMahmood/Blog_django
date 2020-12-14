from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid

##import
from django.views.generic import View, TemplateView, FormView, CreateView, UpdateView, ListView, DetailView, DeleteView

from app_blog.models import Blog, Comment, Likes, CommentLikes
from app_blog.forms import BlogForm, CommentForm

# Create your views here.

class Blog_list (ListView):
    context_object_name = "blogs"
    model = Blog
    template_name = 'app_blog:blog_list.html'
    fields = ('blog_title', 'blog_content', 'blog_image')
    queryset = Blog.objects.order_by('-publish_date')


class Create_blog(LoginRequiredMixin, FormView):
    model = Blog
    form_class = BlogForm
    template_name = 'app_blog/create_blog.html'
    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('app_blog:my_blogs'))

class My_blogs(LoginRequiredMixin, TemplateView):
    template_name = 'app_blog/my_blogs.html'

# class Edit_blog(LoginRequiredMixin, UpdateView):
#     model = Blog
#     fields = ('blog_title', 'blog_content', 'blog_image')
#     template_name = 'app_blog/edit_blog.html'
#
#     def get_success_url(self, **kwargs):
#         return reverse_lazy('app_blog:blog_details', kwargs={'slug':self.object.slug})

class Delete_blog(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'app_blog/delete_blog.html'
    def get_success_url(self):
        return reverse_lazy('app_blog:my_blogs')

@login_required
def edit_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    blog_form = BlogForm(instance=blog)
    dict = {'blog':blog,
            'form':blog_form,
            }

    if request.method =="POST":
        blog_form = BlogForm(request.POST, instance=blog)
        if blog_form.is_valid():
            blog_obj = blog_form.save(commit=False)
            title = blog_obj.blog_title
            blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
            blog_form.save()
            return HttpResponseRedirect(reverse('app_blog:my_blogs'))

    return render(request, 'app_blog/edit_blog.html', context=dict)



@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    liked =False
    already_liked = Likes.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked =True
    if request.method == "POST":
        comment_form = CommentForm( request.POST )
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect( reverse('app_blog:blog_details', kwargs={'slug':slug} ) )

    comment_liked_id=[]
    for comment in blog.blog_comment.filter(user=request.user):
        comment_already_liked = CommentLikes.objects.filter(comment=comment , user=request.user)
        if comment_already_liked:
            comment_liked_id.append(comment.pk)
    dict = {'blog':blog,
            'comment_form':comment_form,
            'liked':liked,
            'comment_liked_id':comment_liked_id,
            }
    return render(request, 'app_blog/blog_details.html', context=dict)


@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post =  Likes(blog=blog, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('app_blog:blog_details', kwargs={'slug':blog.slug} ) )


@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('app_blog:blog_details', kwargs={'slug':blog.slug} ) )


@login_required
def comment_liked(request, pk, pk_comnt):
    blog = Blog.objects.get(pk=pk)
    comment = Comment.objects.get(pk=pk_comnt)
    user = request.user
    comment_already_liked = CommentLikes.objects.filter(comment=comment, user=user)
    if not comment_already_liked:
        liked_comment =  CommentLikes(comment=comment, user=user)
        liked_comment.save()
    return HttpResponseRedirect(reverse('app_blog:blog_details', kwargs={'slug':blog.slug} ) )


@login_required
def comment_unliked(request, pk, pk_comnt):
    blog = Blog.objects.get(pk=pk)
    comment = Comment.objects.get(pk=pk_comnt)
    user = request.user
    comment_already_liked = CommentLikes.objects.filter(comment=comment, user=user)
    comment_already_liked.delete()
    return HttpResponseRedirect(reverse('app_blog:blog_details', kwargs={'slug':blog.slug} ) )
