from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


# Create your models here.

CHOICES = ((0, u"Agree"), (1, u"Partially Agree"), (2, u"Partially Disagree"), (3, u"Disagree"),)

class Answer(models.Model):
    question = models.ForeignKey("Question")

class ChoiceAnswer(Answer):
    answer = models.IntegerField(choices=CHOICES)
    def __unicode__(self):
        return u'%s: %s'%(self.question, self.answer)

class Question(models.Model):
    question = models.CharField(max_length=255)
    answer_type = models.ForeignKey(ContentType,
              limit_choices_to = Q(app_label='home'))

    def __unicode__(self):
        return u'%s'%self.question

#Extension fpr User Profile
class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
