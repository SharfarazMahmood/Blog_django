from django.db import models
########## import django built in models for the database ##################
from django.contrib.auth.models import User



# Create your models here.
############## Create your models here.#######################
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='post_author')
    blog_title = models.CharField( max_length=300, verbose_name = "Title" )
    slug = models.SlugField( max_length=300, unique=True )
    blog_content = models.TextField( verbose_name="Story")
    blog_image = models.ImageField( upload_to='blog_images', verbose_name= "Cover Photo")
    publish_date = models.DateTimeField( auto_now_add=True )
    update_date = models.DateTimeField( auto_now = True )

    class Meta:
        ordering = ['-publish_date',] ## to sort blogs in decending order in list view
    def __str__(self):
        return self.blog_title

class Comment(models.Model):
    blog = models.ForeignKey( Blog, on_delete= models.CASCADE, related_name='blog_comment' )
    user = models.ForeignKey( User, on_delete= models.CASCADE, related_name='user_comment' )
    comment = models.TextField( )
    comment_date = models.DateTimeField( auto_now = True )

    class Meta:
        ordering = ['-comment_date',] ## to sort blogs in decending order in list view
    def __str__(self):
        return self.comment

class Likes(models.Model):
    blog = models.ForeignKey( Blog, on_delete= models.CASCADE, related_name='blog_like' )
    user = models.ForeignKey( User, on_delete= models.CASCADE, related_name='user_like' )

    def __str__(self):
        return self.user + "likes" + self.blog


class CommentLikes(models.Model):
    comment = models.ForeignKey( Comment, on_delete= models.CASCADE, related_name='comment_like' )
    user = models.ForeignKey( User, on_delete= models.CASCADE, related_name='user_comment_like' )

    def __str__(self):
        return str(self.comment)
###############################################################
