from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy 
from django.utils import timezone

import uuid

from django.views.generic import View, TemplateView, FormView, CreateView, UpdateView, ListView, DetailView, DeleteView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from app_blog.models import Blog, Like
from app_blog.forms import BlogForm
from app_comments.models import Comment, CommentLike
from app_comments.forms import CommentForm

from django.contrib.contenttypes.models import ContentType

# Create your views here.


def blog_home(request):
    queryset = Blog.objects.active()

    search_query = request.GET.get("query")
    if search_query:
        queryset = queryset.filter(
                                Q(blog_title__icontains=search_query)|
                                Q(author__username__icontains=search_query)|
                                Q(blog_content__icontains=search_query)
                            ).distinct()

    paginator = Paginator(queryset, 2) # Show 25 contacts per page.
    page_request_var = 'page'
    page_number = request.GET.get(page_request_var)
    page_obj = paginator.get_page(page_number)

    context = {
            'title': 'Posts',
            'blogs': page_obj,
            'page_request_var':page_request_var,
        }
    return render(request, 'app_blog/blog_list.html', context)



class My_blogs(LoginRequiredMixin, TemplateView):
    template_name = 'app_blog/my_blogs.html'


@login_required
def blog_detail(request, id):
    instance = get_object_or_404(Blog, id=id)
    if instance.draft or instance.publish > timezone.now().date() :
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    comments = instance.comments #Comment.objects.filter_by_instance(instance)


    initial_data = {
            "content_type": instance.get_content_type,
            "object_id": instance.id,
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        # c_type = comment_form.cleaned_data.get("content_type")
        c_type =  instance.get_content_type
        content_type = ContentType.objects.get(app_label='app_blog', model='blog')
        object_id = comment_form.cleaned_data.get("object_id")
        parent_obj =None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj = parent_qs.first()

        content_data = comment_form.cleaned_data.get("content")

        new_comment, created = Comment.objects.get_or_create(
                                                    user = request.user,
                                                    content_type = content_type,
                                                    object_id = object_id,
                                                    content = content_data,
                                                    parent = parent_obj
                                                )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
            'blog': instance,
            'title': instance.blog_title,
            'comments': comments,
            'comment_form':comment_form,
        }    
    return render(request, 'app_blog/blog_details.html', context)



@login_required
def blog_create(request):
    form = BlogForm()

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES or None)
        if form.is_valid():
            blog_obj = form.save(commit=False)
            blog_obj.author = request.user
            title = blog_obj.blog_title
            blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
            blog_obj.save()
            messages.success(request, 'Story Created Successfully!! ')
            return HttpResponseRedirect(reverse('app_blog:my_blogs')) 
        else:
            messages.error(request, 'Story create FAILED!! ')

    context = {
        'form':form
    }
    return render(request, 'app_blog/create_blog.html', context)


@login_required
def blog_update(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog_form = BlogForm(instance=blog)

    if request.method =="POST":
        blog_form = BlogForm(request.POST, request.FILES or None,instance=blog)
        if blog_form.is_valid():
            blog_obj = blog_form.save(commit=False)
            title = blog_obj.blog_title
            blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
            blog_form.save()
            messages.success(request, 'Story Updated ! ')
            return HttpResponseRedirect(blog_obj.get_absolute_url())
        else:
            messages.error(request, 'Update FAILED!! ')


    context = {
        'blog':blog,
        'form':blog_form,
    }   
    return render(request, 'app_blog/edit_blog.html', context)


@login_required
def blog_delete(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.delete()
    messages.info(request, 'Story DELETED !!!')
    return redirect('app_blog:my_blogs') 


@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    liked =False
    already_liked = Like.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked =True

    dict = {'blog':blog,
            'liked':liked,
            }
    return render(request, 'app_blog/blog_details.html', context=dict)


@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post =  Like(blog=blog, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('app_blog:blog_detail', kwargs={'id':blog.id} ) )


@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('app_blog:blog_detail', kwargs={'id':blog.id} ) )


