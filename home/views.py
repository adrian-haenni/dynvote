from django.shortcuts import render

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views import generic

from home.forms import UserForm, UserProfileForm, ResponseForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from home.models import Question, Category, Survey, Response, AnswerBase, AnswerRadio, AnswerSelect
from home.utils import generateMatchDict, generateFormInital


# Create your views here.

def index(request):
    return render_to_response('home/index.html', context_instance=RequestContext(request))

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)

            # Did the user provide a group?
            # If so, we need to get it from the post and put it in the User model, empty otherwise.
            user.groups.add(request.POST.get('group', ''))

            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'home/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your DynVote account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('home/login.html', {}, context)

def SurveyDetail(request, id):
    #Obtain the context for the user's request.

    context = RequestContext(request)
    survey = Survey.objects.get(id=id)

    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save(request.user)
            uuid = response.interview_uuid

            return HttpResponseRedirect('/home/confirm/'+uuid)
    else:

        #get inital values
        initialValues = generateFormInital(survey, request.user)

        form = ResponseForm(survey=survey, initial=initialValues)

    return render_to_response('home/survey_detail.html', {'response_form': form, 'survey': survey}, context)

def survey(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    surveys = Survey.objects.all()

    return render_to_response('home/survey.html', {
        'surveys': surveys,
    }, context)

def confirm(request, uuid):
    context = RequestContext(request)

    #check if uuid exists in responses for this user
    if Response.objects.filter(interview_uuid = uuid, user = request.user).exists():
        return render_to_response('home/confirm.html', {'uuid': uuid, 'exists': True, }, context)
    else:
        return render_to_response('home/confirm.html', {'uuid': uuid, 'exists': False, }, context)


def EvaluationDetail(request, uuid):
    context = RequestContext(request)

    userResponse = Response.objects.filter(interview_uuid = uuid, user = request.user)

    #check if uuid exists in responses for this user
    if userResponse.exists():
        surveyOfResponse = Response.objects.get(interview_uuid = uuid, user = request.user).survey
        matchList = generateMatchDict(userResponse, surveyOfResponse)

        return render_to_response('home/evaluation_detail.html', {'uuid': uuid, 'exists': True, 'matchList': matchList, }, context)
    else:

        return render_to_response('home/evaluation_detail.html', {'uuid': uuid, 'exists': False, 'matchList': None, }, context)

def evaluation(request):
    context = RequestContext(request)

    #get evaluations of current user
    responses = Response.objects.filter(user = request.user)

    return render_to_response('home/evaluation.html', {
        'responses': responses,
    }, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')