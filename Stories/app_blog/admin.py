from django.contrib import admin

from app_blog.models import Blog, Like #, Comment, CommentLikes


## to change/customize The ADMIN panel
class BlogModelAdmin(admin.ModelAdmin):
	list_display = ["blog_title", "update_date", "publish_date"]
	list_display_links = ["update_date"]
	list_filter = ["update_date", "publish_date"]
	search_fields = ["blog_title", "blog_content"]
	list_editable = ["blog_title"]
	class Meta:
		model = Blog

# Register your models here.
admin.site.register(Blog, BlogModelAdmin)
admin.site.register(Like)
# admin.site.register(Comment)
