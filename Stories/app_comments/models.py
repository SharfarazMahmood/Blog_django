from django.db import models

# Create your models here.
class Comment(models.Model):
    user        = models.ForiegnKey(settings.AUTH_USER_MODEL)
    blog        =
    content     =
    timestamp   =
