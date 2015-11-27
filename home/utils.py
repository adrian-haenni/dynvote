#Place for helper function

from home.models import Question, Response, AnswerBase, AnswerRadio, AnswerSelect, Survey
from django.contrib.auth.models import User, Group

#check if form was previously filled out by current user, if so, return initial values, empty dict otherwise
def generateFormInital(survey, user):
        #get response if it exists
        previousResponseOfCurrentUser = Response.objects.filter(survey = survey, user = user)

        initialValues = {}

        #get initial data values for form
        if previousResponseOfCurrentUser.exists():

            answerBases = AnswerBase.objects.filter(response = previousResponseOfCurrentUser)

            for answerBase in answerBases:

                if answerBase.question.question_type == Question.RADIO:
                    a = AnswerRadio.objects.get(id=answerBase.id)
                    initialValues["question_%d" % a.question.pk] = a.body

                elif answerBase.question.question_type == Question.SELECT:
                    a = AnswerSelect.objects.get(id=answerBase.id)
                    initialValues["question_%d" % a.question.pk] = a.body

        return initialValues

#generates the matching list over all candidates for a certain response
def generateMatchDict(userResponse, surveyOfResponse):

    answerBasesOfVoter = AnswerBase.objects.filter(response = userResponse)

    #iterate over all candidates (Candidate group name is ugly hard-coded)
    for candidate in User.objects.filter(groups__name='Candidate'):

        #get candidate's response
        candiateResponse = Response.objects.filter(survey = surveyOfResponse, user = candidate)

        #if candidate answered the survey of the user we evaluate
        if candiateResponse.exists():

            #get answers of candidate
            answerBasesOfCandidate = AnswerBase.objects.filter(response = candiateResponse)

            #iterate oveer questions
            

    return None