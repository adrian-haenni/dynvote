from home.models import UserProfile, Response, Question, Survey, AnswerRadio, AnswerSelect
from django.forms import models
from django.contrib.auth.models import User, Group
from django import forms
from django.utils.safestring import mark_safe
import uuid

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class ResponseForm(models.ModelForm):
	class Meta:
		model = Response
		fields = '__all__'
		exclude = ('interview_uuid', 'survey', 'user',)

	def __init__(self, *args, **kwargs):
		# expects a survey object to be passed in initially
		survey = kwargs.pop('survey')
		self.survey = survey
		super(ResponseForm, self).__init__(*args, **kwargs)
		self.uuid = random_uuid = uuid.uuid4().hex

		# add a field for each survey question, corresponding to the question
		# type as appropriate.
		data = kwargs.get('data')
		for q in survey.questions():
			if q.question_type == Question.RADIO:
				question_choices = q.get_choices()

				self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.question,
					widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),
					choices = question_choices)
			elif q.question_type == Question.SELECT:
				question_choices = q.get_choices()
				# add an empty option at the top so that the user has to
				# explicitly select one of the options
				question_choices = tuple([('', '-------------')]) + question_choices

				self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.question,
					widget=forms.Select, choices = question_choices)


			# initialize the form field with values from a POST request, if any.
			if data:
				self.fields["question_%d" % q.pk].initial = data.get('question_%d' % q.pk)

	def save(self, user, commit=True):
		# save the response object
		response = super(ResponseForm, self).save(commit=False)
		response.survey = self.survey
		response.user = user
		response.interview_uuid = self.uuid
		response.save()

		# create an answer object for each question and associate it with this
		# response.
		for field_name, field_value in self.cleaned_data.iteritems():
			if field_name.startswith("question_"):
				# warning: this way of extracting the id is very fragile and
				# entirely dependent on the way the question_id is encoded in the
				# field name in the __init__ method of this form class.
				q_id = int(field_name.split("_")[1])
				q = Question.objects.get(pk=q_id)

				if q.question_type == Question.RADIO:
					a = AnswerRadio(question = q)
					a.body = field_value
				elif q.question_type == Question.SELECT:
					a = AnswerSelect(question = q)
					a.body = field_value
				print "creating answer to question %d of type %s" % (q_id, a.question.question_type)
				print a.question.question
				print 'answer value:'
				print field_value
				a.response = response
				a.save()
		return response

"""
class ChoiceAnswerForm(forms.ModelForm):

    #bar = forms.TypedChoiceField(choices=ChoiceAnswer.CHOICES, widget=forms.RadioSelect, coerce=int)

    class Meta:
        model = ChoiceAnswer
        exclude=("question", )

    def save(self, commit=True):
        # save the response object
        response = super(ChoiceAnswerForm, self).save(commit=False)
        response.interview_uuid = self.uuid
        response.save()

ChoiceAnswer.form = ChoiceAnswerForm
"""


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)

class UserProfileForm(forms.ModelForm):

    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = UserProfile
        fields = ('picture', 'group', )