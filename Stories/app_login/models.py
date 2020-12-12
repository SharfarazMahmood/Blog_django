from django.db import models
########## import django built in models for the database ##################
from django.contrib.auth.models import User

############## Create your models here.#######################
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='UserProfile', on_delete = models.CASCADE)
    profile_pic = models.ImageField( upload_to='profile_pics' )
    # facebook_id = models.URLField(max_length=300, required=False)
###############################################################
