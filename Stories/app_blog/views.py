from django.shortcuts import render

# Create your views here.
def blog_list(request):
    return render(request, 'app_blog/blog_list.html', context={})
