#Place for helper function

from home.models import Question, Response, AnswerBase, AnswerRadio, AnswerSelect, Survey, AskBase, CustomQuestion
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

            setOfAllAnsweredQuestionIDs = set()

            for answerBase in answerBases:
                if answerBase.question.question_type == Question.RADIO:
                    a = AnswerRadio.objects.get(id=answerBase.id)
                    initialValues["question_%d" % a.question.pk] = a.body
                    setOfAllAnsweredQuestionIDs.add(a.question.pk)

                elif answerBase.question.question_type == Question.SELECT:
                    a = AnswerSelect.objects.get(id=answerBase.id)
                    initialValues["question_%d" % a.question.pk] = a.body
                    setOfAllAnsweredQuestionIDs.add(a.question.pk)

            unansweredQuestion = survey.questions().exclude(pk__in = setOfAllAnsweredQuestionIDs)

            for q in unansweredQuestion:
                initialValues["question_%d" % q.pk] = "No Answer"

        #if response does not exists fill out with "No Answer"
        else:
            for question in survey.questions():
                initialValues["question_%d" % question.pk] = "No Answer"

        return initialValues

#generates the matching list over all candidates for a certain response
def generateMatches(userResponse, surveyOfResponse):

    answerBasesOfUser = AnswerBase.objects.filter(response = userResponse)

    matchResults = []

    #iterate over all candidates (Candidate group name is ugly hard-coded)
    for candidate in User.objects.filter(groups__name='Candidate'):

        #get candidate's response
        candiateResponse = Response.objects.filter(survey = surveyOfResponse, user = candidate)

        numOfSameAnswersForThisCandidate = 0
        numOfCountedComparedAnswers = 0

        #if candidate answered the survey of the user we evaluate
        if candiateResponse.exists():

            #get answers of candidate
            answerBasesOfCandidate = AnswerBase.objects.filter(response = candiateResponse)

            #if user is candidate, do not compare his results to his own again
            if userResponse[0].user.pk != candiateResponse[0].user.pk:

                #iterate over questions
                for candidateAnswerBase in answerBasesOfCandidate:

                    for userAnswerBase in answerBasesOfUser:

                        #compare same questions
                        if userAnswerBase.question.pk is candidateAnswerBase.question.pk:

                            print "======================="
                            print "WILL CHECK ANSWERS FOR:"
                            print "User:\t\t %s" % userAnswerBase.response.user.username
                            print "Candidate:\t %s" % candidateAnswerBase.response.user.username


                            #check if question is a custom question, if so, check if it has been approved by candidate and voter/candidate
                            if CustomQuestion.objects.filter(pk=userAnswerBase.question.pk).exists():

                                customQuestion = CustomQuestion.objects.get(pk=userAnswerBase.question.pk)

                                bothApproved = checkForApprovance(customQuestion, userResponse[0].user.pk, candiateResponse[0].user.pk)
                                if bothApproved:
                                    print "BOTH APPROVED"
                                    sameAnswer, bothIsNoAnswer, atLeastOneIsNoAnswer  = checkForSameAnswer(userAnswerBase, candidateAnswerBase)

                                    if bothIsNoAnswer:
                                        break
                                    elif sameAnswer:
                                        numOfCountedComparedAnswers += 1
                                        numOfSameAnswersForThisCandidate += 1
                                    elif not atLeastOneIsNoAnswer:
                                        numOfCountedComparedAnswers += 1

                                    break

                            else:

                                sameAnswer, bothIsNoAnswer, atLeastOneIsNoAnswer  = checkForSameAnswer(userAnswerBase, candidateAnswerBase)

                                if bothIsNoAnswer:
                                    break
                                elif sameAnswer:
                                    numOfCountedComparedAnswers += 1
                                    numOfSameAnswersForThisCandidate += 1
                                elif not atLeastOneIsNoAnswer:
                                    numOfCountedComparedAnswers += 1

                                break

                #TO DO
                """
                numOfCandidateAnswersWithoutNoAnswer = 0
                for answerBaseToCount in answerBasesOfCandidate:
                    if answerBaseToCount.question.question_type == Question.RADIO:
                        a = AnswerRadio.objects.get(id=answerBaseToCount.id)
                        if a.body != "No Answer":
                            numOfCandidateAnswersWithoutNoAnswer += 1

                    elif answerBaseToCount.question.question_type == Question.SELECT:
                        a = AnswerSelect.objects.get(id=answerBaseToCount.id)
                        if a.body != "No Answer":
                            numOfCandidateAnswersWithoutNoAnswer += 1
                """


                print "NUMBER of compared answers: %d" % numOfCountedComparedAnswers
                print "NUMBER of same answers: %d" % numOfSameAnswersForThisCandidate

                percentage = getPercentage(numOfSameAnswersForThisCandidate, numOfCountedComparedAnswers)
                print "percentage %d" % percentage

                #create the dict
                dict = {'candidate': candidate,
                        'percentage': percentage,
                        'totalAnswers': numOfCountedComparedAnswers,
                        }

                matchResults.append(dict)

    sortedMatchResults = sorted(matchResults, key=itemgetter('percentage'), reverse=True)

    return sortedMatchResults


def checkForSameAnswer(userAnswerBase, candidateAnswerBase):

    sameAnswer = False
    bothIsNoAnswer = False
    atLeastOneIsNoAnswer = False

    if userAnswerBase.question.question_type == Question.RADIO:
        a = AnswerRadio.objects.get(id=userAnswerBase.id)
        c = AnswerRadio.objects.get(id=candidateAnswerBase.id)
        #print "user answer: %s" % a.body
        #print "cand answer: %s" % c.body

    elif userAnswerBase.question.question_type == Question.SELECT:
        a = AnswerSelect.objects.get(id=userAnswerBase.id)
        c = AnswerSelect.objects.get(id=candidateAnswerBase.id)
        #print "user answer: %s" % a.body
        #print "cand answer: %s" % c.body

    if (a.body == "No Answer") or (c.body == "No Answer"):
        print "One answered with No Answer"
        atLeastOneIsNoAnswer = True

    if a.body == c.body:
        print "Same Answer"
        sameAnswer = True
        if a.body == "No Answer":
            bothIsNoAnswer = True

    return (sameAnswer, bothIsNoAnswer, atLeastOneIsNoAnswer)

def checkForApprovance(customQuestion, userPK, candidatePK):
    print "customQuestion: %s" % customQuestion.question[0:24]+"..."

    isApprovedByUser = False
    isApprovedByCandidate = False

    #iterate over askBases for this custom question, check if they are currently approved
    for askBase in customQuestion.askbase_set.all():
        if askBase.isAccepted == True and askBase.user.pk == userPK:
            isApprovedByUser = True
        elif askBase.isAccepted == True and askBase.user.pk == candidatePK:
            isApprovedByCandidate = True

        if isApprovedByUser and isApprovedByCandidate:
            return True

    return False

def getPercentage(hits, total):

    if total == 0:
        return int(0)

    percentage = float(hits) / float(total)
    return int(percentage * 100)

def createAskBasesForUsers(users, userWhoAsked, customQuestion):

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

def getUnaskedUsers(customQuestion):
    unaskedUsers = set()

    for user in User.objects.all():
        if not AskBase.objects.filter(customQuestion=customQuestion, user=user).exists():
            unaskedUsers.add(user.pk)

    return User.objects.filter(pk__in = unaskedUsers)

#append own user to list of asked users
def appendOwnUserToAskedUser(ownUser, askedUsers):
    wantedUsers = set()
    for user in askedUsers:
        wantedUsers.add(user.pk)

    wantedUsers.add(ownUser.pk)

    return User.objects.filter(pk__in = wantedUsers)

def registerNewUserToAllCandidateQuestions(user):
    for customQuestion in CustomQuestion.objects.all():
        if customQuestion.creator.groups.filter(name='Candidate').exists():
            askBase = AskBase(customQuestion=customQuestion, user=user)
            askBase.isAccepted = False
            askBase.save()