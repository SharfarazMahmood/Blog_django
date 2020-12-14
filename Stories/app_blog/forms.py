from django import forms
from pagedown.widgets import PagedownWidget
from app_blog.models import Blog, Comment


class BlogForm(forms.ModelForm):
    blog_content = forms.CharField(widget=PagedownWidget())
    class Meta():
        model = Blog
        fields = ('blog_title', 'blog_content', 'blog_image',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
