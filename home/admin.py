# Import the UserProfile model individually.
from django.contrib import admin

from home.models import UserProfile
from .models import Question, Category, Survey, Response, AnswerBase, AnswerRadio, AnswerSelect, CustomQuestion, AskBase

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(Response)
admin.site.register(AnswerBase)
admin.site.register(AnswerRadio)
admin.site.register(AnswerSelect)
admin.site.register(CustomQuestion)
admin.site.register(AskBase)