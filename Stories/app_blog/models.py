from django.db import models
########## import django built in models for the database ##################
from django.contrib.auth.models import User

# Create your models here.
############## Create your models here.#######################
class Blog(models.Model):
    author = models.ForeignKey(User, related_name='post_author', on_delete = models.CASCADE)
    blog_title = models.CharField( max_length=252, verbose_name = "Add Title" )
    slug = models.SlugField( max_length=252, unique=True )
    blog_content = models.TextField( verbose_name="Share a Story" )
    blog_image = models.ImageField( upload_to='blog_images', verbose_name= "Add Cover Photo")
    publish_date = models.DateTimeField( auto_now_add=True )
    update_date = models.DateTimeField( auto_now = True )

    def __str__(self):
        return self.blog_title

class Comment(models.Model):
    blog = models.ForeignKey( Blog, on_delete= models.CASCADE, related_name='blog_comment' )
    user = models.ForeignKey( User, on_delete= models.CASCADE, related_name='user_comment' )
    comment = models.TextField( )
    comment_date = models.DateTimeField( auto_now = True )

    def __str__(self):
        return self.comment

class Likes(models.Model):
    blog = models.ForeignKey( Blog, on_delete= models.CASCADE, related_name='blog_like' )
    user = models.ForeignKey( User, on_delete= models.CASCADE, related_name='user_like' )

class CommentLikes(models.Model):
    blog = models.ForeignKey( Blog, on_delete= models.CASCADE, related_name='comment_like' )
    user = models.ForeignKey( User, on_delete= models.CASCADE, related_name='user_comment_like' )
###############################################################
