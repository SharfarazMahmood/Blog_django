from django.contrib import admin

from app_comments.models import Comment, CommentLike


# Register your models here.
admin.site.register(Comment)
admin.site.register(CommentLike)