from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
import uuid
import os

def get_image_file_name(instance,filename):

    ext=filename.split('.')[-1]
    filename="{}.{}".format(uuid.uuid4(),ext)

    return os.path.join('profile_pics/',filename)

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})



class User(AbstractUser):
    is_admin=models.BooleanField(default=False,help_text='Designates whether the user has admin permissions.', verbose_name='admin status')
    profile_pic=models.ImageField(upload_to=get_image_file_name,blank=True,null=True)

    objects=CustomUserManager()