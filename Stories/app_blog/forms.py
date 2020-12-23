from django import forms
from functools import partial
from pagedown.widgets import PagedownWidget
from app_blog.models import Blog #, Comment


class BlogForm(forms.ModelForm):
    # blog_content = forms.CharField(widget=PagedownWidget())
    publish = forms.DateField( widget=forms.TextInput(attrs={'type':'Date'}) )
    class Meta():
        model = Blog
        fields = ('blog_title', 
        			'blog_content', 
        			'blog_image',
        			'draft',
        			'publish',
        		)


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('comment',)
