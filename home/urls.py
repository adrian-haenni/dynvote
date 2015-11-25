from django.conf.urls import url
from django.conf import settings


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^survey/$', views.survey, name='survey'),
    url(r'^survey/(?P<id>\d+)/$', views.SurveyDetail, name='survey_detail'),
    url(r'^evaluation/$', views.evaluation, name='evaluation'),
    url(r'^evaluation/(?P<id>\d+)/$', views.EvaluationDetail, name='evaluation_detail'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
]
