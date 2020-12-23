from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# from app_blog.models import Blog 
# Create your models here.
class CommentManager(models.Manager):
	def all(self):
		qs = super(CommentManager, self). filter(parent = None)
		return qs
	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		object_id = instance.id
		query_set = super(CommentManager, self).filter(content_type=content_type, object_id=object_id).filter(parent=None)
		return query_set



class Comment(models.Model):
	user 			= models.ForeignKey(User, on_delete = models.CASCADE, related_name='commenter')

	#story		= models.ForeignKey(Blog, on_delete = models.CASCADE, related_name='commented_on')
	content_type 	= models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id 		= models.PositiveIntegerField()
	content_object 	= GenericForeignKey('content_type', 'object_id')
	
	parent 			= models.ForeignKey("self",on_delete=models.CASCADE, null=True, blank=True)

	content			= models.TextField(max_length=160)
	timestamp		= models.DateTimeField(auto_now_add=True)


	objects = CommentManager()

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return str(self.content)+ ' by '+str(self.user.username)

	def children(self): ## replies 
		return Comment.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True


class CommentLike(models.Model):
    comment		= models.ForeignKey( Comment, on_delete= models.CASCADE, related_name='comment_like' )
    user		= models.ForeignKey( User, on_delete= models.CASCADE, related_name='comment_liker' )

    def __str__(self):
        return str(self.comment)