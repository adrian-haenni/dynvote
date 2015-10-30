from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#The Django ImageField field makes use of the Python Imaging Library (PIL). Installing PIL along with Django to your setup. If you haven't got PIL installed, you'll need to install it now. If you don't, you'll be greeted with exceptions stating that the module pil cannot be found!
#Do it with 'pip install pil'

class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
