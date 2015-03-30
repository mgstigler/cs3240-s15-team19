from django.conf.urls import patterns, url
from secure_witness import views

urlpatterns = patterns('',
    #/secure_witness/'
    # TODO Decide on an index page
    #/secure_witness/register
    url(r'^register/$', views.register, name='register'),
    #/secure_witness/login
    url(r'^login/$', views.user_login, name='login'),
    )