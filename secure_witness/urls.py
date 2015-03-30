from django.conf.urls import patterns, url
from secure_witness import views

urlpatterns = patterns('',
    #/secure_witness/register
    url(r'^register/$', views.register, name='register'),
    )