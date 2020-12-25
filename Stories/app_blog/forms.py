from django import forms
from functools import partial
from app_blog.models import Blog #, Comment


class BlogForm(forms.ModelForm):
    publish = forms.DateField( widget=forms.TextInput(attrs={'type':'Date'}) )
    class Meta():
        model = Blog
        fields = ('blog_title', 
        			'blog_content', 
        			'blog_image',
        			'draft',
        			'publish',
        		)