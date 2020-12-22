from django.db import models
from django.urls import reverse
from django.utils import timezone
########## import django built in models for the database ##################
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


## MVC model view 
# Create your models here.
############## Create your models here.#######################
class BlogManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(BlogManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return "%s/%s" %(instance.author, filename)



class Blog(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='post_author')
    blog_title = models.CharField( max_length=300, verbose_name = "Title" )
    slug = models.SlugField( max_length=320, unique=True )
    # blog_content = models.TextField( verbose_name="Story")
    blog_content = RichTextField(verbose_name="Story")

    ##### following needs the PILLOW package to work
    blog_image = models.ImageField( upload_to=upload_location, 
                                    null=True, 
                                    blank=True, 
                                    verbose_name= "Cover Photo")
    # blog_image = models.FileField( null=True, blank=True, verbose_name= "Cover Photo")

    publish_date = models.DateTimeField( auto_now_add=True )
    update_date = models.DateTimeField( auto_now = True )
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False , auto_now_add=False)

    objects = BlogManager()

    class Meta:
        ordering = ['-publish', '-update_date'] ## to sort blogs in decending order in list view
    def __str__(self):
        return self.blog_title
    def get_absolute_url(self):
        return reverse('app_blog:blog_detail', kwargs={'id':self.id})
        # return "detail/%s/" %(self.id)




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
        return str(self.user) + " likes " + str(self.blog)


class CommentLikes(models.Model):
    comment = models.ForeignKey( Comment, on_delete= models.CASCADE, related_name='comment_like' )
    user = models.ForeignKey( User, on_delete= models.CASCADE, related_name='user_comment_like' )

    def __str__(self):
        return str(self.comment)
###############################################################
