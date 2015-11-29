from home.models import UserProfile, Response, Question, Survey, AnswerRadio, AnswerSelect, CustomQuestion
from django.forms import models
from django.contrib.auth.models import User, Group
from django import forms
from django.utils.safestring import mark_safe
import uuid
from home.utils import createAskBasesForUsers, getOtherUsers, appendOwnUserToAskedUser
from django.contrib.admin.widgets import FilteredSelectMultiple

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class AskFormForCandidates(models.ModelForm):
	class Meta:
		model = CustomQuestion
		fields = '__all__'
		exclude = ('creator','question_type', 'choices', )

	def __init__(self, *args, **kwargs):

		user = kwargs.pop('user')

		super(AskFormForCandidates, self).__init__(*args, **kwargs)

	def save(self, user, commit=True):

		customQuestion = super(AskFormForCandidates, self).save(commit=False)
		customQuestion.creator = user
		customQuestion.question_type = Question.RADIO
		customQuestion.choices = 'Agree, Partially Agree, Partially Disagree, Disagree'
		customQuestion.save()

		createAskBasesForUsers(User.objects.all(), user, customQuestion)

		return customQuestion


class AskFormForVoter(models.ModelForm):

	users_to_ask = forms.ModelMultipleChoiceField('users_to_ask')

	class Meta:
		model = CustomQuestion
		fields = '__all__'
		exclude = ('creator','question_type', 'choices', )

	class Media:
		css = {'all': ('/static/admin/css/widgets.css',),}
		#js = ('/static/admin/js/jquery.js', '/static/admin/js/jquery.init.js', '/admin/jsi18n', '/static/admin/js/related-widget-wrapper.js',)

	def __init__(self, *args, **kwargs):

		user = kwargs.pop('user')

		super(AskFormForVoter, self).__init__(*args, **kwargs)

		self.fields['users_to_ask'] = forms.ModelMultipleChoiceField(widget=FilteredSelectMultiple("Users", is_stacked=False),
											  label=('Select Users'),
											  queryset=getOtherUsers(user),
											  required=True)

	def save(self, user, commit=True):

		customQuestion = super(AskFormForVoter, self).save(commit=False)
		customQuestion.creator = user
		customQuestion.question_type = Question.RADIO
		customQuestion.choices = 'Agree, Partially Agree, Partially Disagree, Disagree, No Answer'
		customQuestion.save()

		#generate AskBases for asked user and include self
		askedUsers = self.cleaned_data['users_to_ask']
		print "the following users have been asked:"
		for askedUser in askedUsers:
			print "username: %s" % askedUser.username

		usersToForwardQuestionTo = appendOwnUserToAskedUser(user, askedUsers)

		createAskBasesForUsers(usersToForwardQuestionTo, user, customQuestion)

		return customQuestion

class AskBasesForm(forms.Form):

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		self.askBases = kwargs.pop('askBases')

		super(AskBasesForm, self).__init__(*args, **kwargs)

		for askBase in self.askBases:
			#if self.user.pk != askBase.customQuestion.creator.pk:
			self.fields["question_%d" % askBase.customQuestion.pk] = forms.BooleanField(label=askBase.customQuestion.question,
																						initial=askBase.isAccepted,
																						required=False)
				#self.fields["question_%d" % askBase.customQuestion.pk].widget.attrs['onclick'] = "return false"
			if self.user.pk != askBase.customQuestion.creator.pk:
				self.fields["question_%d" % askBase.customQuestion.pk].help_text = askBase.customQuestion.creator.username
			else:
				self.fields["question_%d" % askBase.customQuestion.pk].help_text = "yourself"

	def save(self, commit=True):
		for askBase in self.askBases:
			boolValueForQuestion = self.cleaned_data['question_%d' % askBase.customQuestion.pk]
			askBase.isAccepted = boolValueForQuestion
			askBase.save()

class ResponseForm(models.ModelForm):
	class Meta:
		model = Response
		fields = '__all__'
		exclude = ('interview_uuid', 'survey', 'user',)

	def __init__(self, *args, **kwargs):
		# expects a survey object to be passed in initially
		survey = kwargs.pop('survey')
		self.survey = survey
		currentUser = kwargs.pop('currentUser')
		self.currentUser = currentUser
		super(ResponseForm, self).__init__(*args, **kwargs)
		self.uuid = random_uuid = uuid.uuid4().hex

		# add a field for each survey question, corresponding to the question
		# type as appropriate.
		data = kwargs.get('data')
		for q in survey.questions():

			#Add special treatment for question objects that are also custom questions
			if CustomQuestion.objects.filter(pk=q.pk).exists():
				#"cast" to CustomQuestion Class
				customQuestion = CustomQuestion.objects.get(pk=q.pk)
				for askBase in customQuestion.askbase_set.all():
					if askBase.isAccepted == True and askBase.user.pk == self.currentUser.pk:
						print "%s did approve question id %d" % (askBase.user.username, customQuestion.id)

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

			#question is not a custom question, then include in survey
			else:
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

		#check if user already has answered this survey
		#TO DO: Refacter do not create new object but rather update one
		oldResponse = Response.objects.filter(user = user, survey = self.survey)
		num_results = oldResponse.count()
		#each save assures that there can only be only response object for a user for a survey (important in other methods)
		if num_results > 0:
			print 'as user already has answered this survey, system is going to delete old response object(s)'
			for x in range(0, num_results):
				delete = Response.objects.get(pk=oldResponse[x].id).delete()

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