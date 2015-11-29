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
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^ask/(?P<id>\d+)/$', views.AskDetail, name='ask_detail'),
    url(r'^approve/$', views.approve, name='approve'),
    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^evaluation/$', views.evaluation, name='evaluation'),
    url(r'^evaluation/(?P<uuid>[0-9A-Za-z]{,36})/$', views.EvaluationDetail, name='evaluation_detail'),
    url(r'^confirm/(?P<uuid>[0-9A-Za-z]{,36})/$', views.confirm, name='confirm'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
]
