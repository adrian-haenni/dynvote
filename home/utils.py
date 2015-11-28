#Place for helper function

from home.models import Question, Response, AnswerBase, AnswerRadio, AnswerSelect, Survey, AskBase
from django.contrib.auth.models import User, Group
from operator import itemgetter

#check if form was previously filled out by current user, if so, return initial values, empty dict otherwise
def generateSurveyFormInital(survey, user):
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

def generateAskBasesFormInital(user):

    return None

#generates the matching list over all candidates for a certain response
def generateMatches(userResponse, surveyOfResponse):

    answerBasesOfUser = AnswerBase.objects.filter(response = userResponse)

    matchResults = []

    #iterate over all candidates (Candidate group name is ugly hard-coded)
    for candidate in User.objects.filter(groups__name='Candidate'):

        #get candidate's response
        candiateResponse = Response.objects.filter(survey = surveyOfResponse, user = candidate)

        numOfSameAnswersForThisCandidate = 0

        #if candidate answered the survey of the user we evaluate
        if candiateResponse.exists():

            #get answers of candidate
            answerBasesOfCandidate = AnswerBase.objects.filter(response = candiateResponse)

            #if user is candidate, do not compare his results to his own again
            #TODO

            #iterate over questions
            for candidateAnswerBase in answerBasesOfCandidate:

                for userAnswerBase in answerBasesOfUser:

                    #compare same questions
                    if userAnswerBase.question.pk is candidateAnswerBase.question.pk:

                        print "user %s" % userAnswerBase.response.user.username
                        print "cand %s" % candidateAnswerBase.response.user.username

                        if userAnswerBase.question.question_type == Question.RADIO:
                            a = AnswerRadio.objects.get(id=userAnswerBase.id)
                            c = AnswerRadio.objects.get(id=candidateAnswerBase.id)
                            print "user answer: %s" % a.body
                            print "cand answer: %s" % c.body

                        elif userAnswerBase.question.question_type == Question.SELECT:
                            a = AnswerSelect.objects.get(id=userAnswerBase.id)
                            c = AnswerSelect.objects.get(id=candidateAnswerBase.id)
                            print "user answer: %s" % a.body
                            print "cand answer: %s" % c.body

                        if a.body == c.body:
                            print "SAME ANSWER"
                            numOfSameAnswersForThisCandidate += 1

                        break

            numOfCandidateAnswers = answerBasesOfCandidate.count()
            print "NUMBER of answers: %d" % numOfCandidateAnswers
            print "NUMBER of same answers: %d" % numOfSameAnswersForThisCandidate

            percentage = getPercentage(numOfSameAnswersForThisCandidate, numOfCandidateAnswers)
            print "percentage %d" % percentage

            #create the dict
            dict = {'candidate': candidate,
                    'percentage': percentage,
                    }

            matchResults.append(dict)

    sortedMatchResults = sorted(matchResults, key=itemgetter('percentage'), reverse=True)

    return sortedMatchResults

def getPercentage(hits, total):
    percentage = float(hits) / float(total)
    return int(percentage * 100)

def createAskBasesForUsers(users ,userWhoAsked, customQuestion):

    for user in users:
        askBase = AskBase(customQuestion=customQuestion, user=user)
        if userWhoAsked.pk == user.pk:
            askBase.isAccepted = True
        else:
            askBase.isAccepted = False

        #print "creating ask base for %s for question %s" % (user.username, customQuestion.question)
        askBase.save()

#get all users except self
def getOtherUsers(user):
    return User.objects.exclude(pk=user.pk)

#append own user to list of asked users
def appendOwnUserToAskedUser(ownUser, askedUsers):
    wantedUsers = set()
    for user in askedUsers:
        wantedUsers.add(user.pk)

    wantedUsers.add(ownUser.pk)

    return User.objects.filter(pk__in = wantedUsers)