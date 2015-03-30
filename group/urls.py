from django.conf.urls import patterns, include, url
from django.contrib import admin
from secure_witness.views import report, submit

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'group.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^report/', report),
    url(r'^submit$', submit)

)
