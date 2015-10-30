from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
]
