from django.conf.urls import patterns, include, url
from django.contrib import admin
from secure_witness.views import report, submit

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'group.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^report/', report),
    url(r'^submit$', submit),

    # secure_witness app urls
    url(r'^secure_witness/', include('secure_witness.urls', namespace="secure_witness"))
)
