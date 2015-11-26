#Place for helper function

from home.models import Question, Response, AnswerBase, AnswerRadio, AnswerSelect

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

def generateMatchDict(userResponse):



    return None