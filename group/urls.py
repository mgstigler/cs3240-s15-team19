from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import secure_witness.views


urlpatterns = patterns('',
    url(r'^$', secure_witness.views.ListFolderView.as_view(),
        name='folders-list',),
    url(r'^new$', secure_witness.views.CreateFolderView.as_view(),
        name='folders-new',),
    url(r'^edit/(?P<pk>\d+)/$', secure_witness.views.UpdateFolderView.as_view(),
        name='folders-edit',),
    url(r'^delete/(?P<pk>\d+)/$', secure_witness.views.DeleteFolderView.as_view(),
        name='folders-delete',),
    url(r'^(?P<pk>\d+)/$', secure_witness.views.FolderView.as_view(),
        name='folders-view',),
    url(r'^edit/(?P<pk>\d+)/files$', secure_witness.views.EditFolderFileView.as_view(),
        name='folders-edit-files',),
)

urlpatterns += staticfiles_urlpatterns()