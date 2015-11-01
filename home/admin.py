# Import the UserProfile model individually.
from django.contrib import admin

from home.models import UserProfile
from .models import Question

admin.site.register(Question)