from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
import secure_witness.views
from secure_witness.views import saved




urlpatterns = patterns('',
    #/admin/
    url(r'^admin/', include(admin.site.urls)),
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
    #/rep/1/add-comment
    url(r'^rep/(?P<report_id>\d+)/add-comment$', secure_witness.views.add_comment,
        name='report-add-comment'),
    #/rep/1/edit-comment/2
    url(r'^rep/(?P<report_id>\d+)/edit-comment/(?P<pk>\d+)/$', secure_witness.views.CommentUpdateView.as_view(),
        name='report-edit-comment'),
    #/rep/1/delete-comment/2
    url(r'rep/(?P<report_id>\d+)/delete-comment/(?P<pk>\d+)/$', secure_witness.views.CommentDeleteView.as_view(),
        name='report-delete-comment'),
    #/rep/1/delete-file/2
    url(r'rep/(?P<report_id>\d+)/delete-media/(?P<media_id>\d+)/$', secure_witness.views.media_delete,
        name='media-delete'),

    #/deleterep/5/    
    url(r'^deleterep/(?P<pk>\d+)/$', secure_witness.views.DeleteReportView.as_view(),
        name='reports-delete',),

    url(r'^editrep/(?P<pk>\d+)/$', secure_witness.views.UpdateReportView.as_view(),
        name='report-edit',),
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
   

    #/browse/
    url(r'browse/(?P<folder_id>\d+)?$', secure_witness.views.JointFolderReportView.as_view(),
        name='browse'),
    url(r'user-manager/$', secure_witness.views.AdminUserManager.as_view(),
        name='user-manager'),
    url(r'user-manager/(?P<user_id>\d+)$', secure_witness.views.switch_user_active,
        name='user-manager-activate'),
    url(r'edit-profile/$', secure_witness.views.edit_profile,
        name='edit-profile'),
    url(r'^download/(?P<pk>\d+)/$', secure_witness.views.downloadfiles,
        name='download'),

    #/register/
    url(r'^register/$', secure_witness.views.register_user, name='register-user'),
    #/confirm/111
    url(r'confirm/(?P<activation_key>\w+)/$', secure_witness.views.register_confirm, name='register-confirm'),

    #/advanced-search/
    url(r'^advanced-search/$', secure_witness.views.advanced_search, name='advanced-search'),

    url(r'json_test/$', secure_witness.views.json_test, name='json-test'),

)

urlpatterns += staticfiles_urlpatterns()
