from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import secure_witness.views

from django.contrib import admin
from secure_witness.views import report, submit




urlpatterns = patterns('',
    #/admin/
    url(r'^admin/', include(admin.site.urls)),
    #/
    url(r'^$', secure_witness.views.ListFolderView.as_view(),
        name='folders-list',),
    #/new/
    url(r'^new$', secure_witness.views.CreateFolderView.as_view(),
        name='folders-new',),
    #/edit/1/
    url(r'^edit/(?P<pk>\d+)/$', secure_witness.views.UpdateFolderView.as_view(),
        name='folders-edit',),
    #/delete/1/
    url(r'^delete/(?P<pk>\d+)/$', secure_witness.views.DeleteFolderView.as_view(),
        name='folders-delete',),
    #/1/
    url(r'^(?P<pk>\d+)/$', secure_witness.views.FolderView.as_view(),
        name='folders-view',),
    #/edit/1/files
    url(r'^edit/(?P<pk>\d+)/files$', secure_witness.views.EditFolderFileView.as_view(),
        name='folders-edit-files',),
    #/report/
    url(r'^report/', report),
    #/submit/
    url(r'^submit$', submit),
    #/register/
    url(r'^register/$', secure_witness.views.register, name='register'),
    #/login/
    url(r'^login/$', secure_witness.views.user_login, name='login'),

)

urlpatterns += staticfiles_urlpatterns()
