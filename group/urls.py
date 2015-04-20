from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin

import secure_witness.views
from secure_witness.views import saved




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
    #/1/report/
    url(r'^report/$', secure_witness.views.CreateReportView.as_view(),
        name='reports-new',), 

    #saved
    url(r'^saved/$', saved,
        name='saved',), 
    url(r'^copy/(?P<pk>\d+)/$', secure_witness.views.copy, name='copy'),

    #/rep/5/
    url(r'^rep/(?P<pk>\d+)/$', secure_witness.views.ReportView.as_view(),
        name='report-detail',),

    #/deleterep/5/    
    url(r'^deleterep/(?P<pk>\d+)/$', secure_witness.views.DeleteReportView.as_view(),
        name='reports-delete',),

    url(r'^editrep/(?P<pk>\d+)/$', secure_witness.views.UpdateReportView.as_view(),
        name='report-edit',),
    #/report/
    #url(r'^report/', report, name='report-new'),
    #/submit/
    #url(r'^submit$', submit),
    #/register/
    url(r'^register/$', secure_witness.views.register, name='register'),
    #/login/
    url(r'^login/$', secure_witness.views.user_login, name='login'),
    #/logout/
    url(r'^logout/$', secure_witness.views.user_logout, name='logout'),
    #/groups/
    url(r'^groups/list/$', secure_witness.views.GroupListView.as_view(),
        name='group-list'),
    #/groups/1
    url(r'^groups/(?P<pk>\d+)/$', secure_witness.views.GroupDetailView.as_view(),
        name='group-detail'),
    #/groups/1/edit
    url(r'^groups/(?P<pk>\d+)/edit/$', secure_witness.views.GroupEditView.as_view(),
        name='group-edit'),
    #/groups/1/delete
    url(r'^groups/delete/(?P<pk>\d+)/delete$', secure_witness.views.GroupDeleteView.as_view(),
        name='group-delete'),
    #/groups/create
    url(r'^groups/create/$', secure_witness.views.GroupCreateView.as_view(),
        name='group-create'),
    #/groups/1/edit/add-user
    url(r'^groups/(?P<group_id>\d+)/edit/add-user/$', secure_witness.views.add_user,
        name='group-add-user'),
    #/groups/1/edit/remove-user/1
    url(r'^groups/(?P<group_id>\d+)/edit/remove-user/(?P<user_id>\d+)/$', secure_witness.views.remove_user,
        name='group-remove-user'),
    url(r'^search/$', secure_witness.views.search, name='search' ),
   

)

urlpatterns += staticfiles_urlpatterns()
