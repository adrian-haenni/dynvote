from django.db import models
from django.contrib.auth.models import User

# Create your models here.

RATING_CHOICES = ((0, u"Agree"), (1, u"Partially Agree"), (2, u"Partially Disagree"), (3, u"Disagree"),)


class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
