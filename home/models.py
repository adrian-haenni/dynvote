from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.exceptions import ValidationError


# Create your models here.

#The object of a single survey e.g. Nationalratswahlen 15
class Survey(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return u'%s'%self.name

    #returns all questions of this survey ordered by category
    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk).order_by('category_type')
        else:
            return None

#A category that has to be associated by a question
class Category(models.Model):
    category = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s'%self.category

def validate_list(value):
    #takes a text value and verifies that there is at least one comma
    values = value.split(',')
    if len(values) < 2:
        raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")


#A single question
class Question(models.Model):
    RADIO = 'radio'
    SELECT = 'select'
    QUESTION_TYPES = (
        (RADIO, 'radio'),
        (SELECT, 'select'),
    )

    question = models.CharField(max_length=255)
    category_type = models.ForeignKey("Category", null=True)
    survey = models.ForeignKey(Survey, null=True)

    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=RADIO)

    choices = models.TextField(blank=True, null=True,
                               help_text='if the question type is "radio," or "select,"')

    def save(self, *args, **kwargs):
        if (self.question_type == Question.RADIO or self.question_type == Question.SELECT):
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        ''' parse the choices field and return a tuple formatted appropriately
		for the 'choices' argument of a form widget.'''
        choices = self.choices.split(',')
        choices_list = []
        for c in choices:
			c = c.strip()
			choices_list.append((c,c))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __unicode__(self):
        return u'%s'%self.question

# a response object is just a collection of questions and answers with a unique interview uuid
class Response(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    survey = models.ForeignKey(Survey)

    user = models.ForeignKey(User, null=True)

    interview_uuid = models.CharField("Interview unique identifier", max_length=36)

    def __unicode__(self):
        return ("response %s" % self.interview_uuid)

class AnswerBase(models.Model):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class AnswerRadio(AnswerBase):
    body = models.TextField(blank=True, null=True)

class AnswerSelect(AnswerBase):
    body = models.TextField(blank=True, null=True)

class CustomQuestion(Question):
    creator = models.ForeignKey(User)

class AskBase(models.Model):
    customQuestion = models.ForeignKey(Question, null=True)
    user = models.ForeignKey(User, null=True)
    isAccepted = models.BooleanField()

    def __unicode__(self):
        return u'%s - %s'%(self.customQuestion.question, self.user.username)


#Extension for User Profile
class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
