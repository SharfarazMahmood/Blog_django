from django.contrib import admin

############# import all the models ################
from app_blog.models import Blog, Comment, Likes, CommentLikes

# Register your models here.
admin.site.register(Blog)
admin.site.register(Likes)
admin.site.register(Comment)
admin.site.register(CommentLikes)