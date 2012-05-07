from django.conf.urls.defaults import patterns, include, url
from konsultacje import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'consultations.views.consultation_index'),
	url(r'^authorization/$', 'consultations.views.authorization'),
	url(r'^choosepanel/(?P<user_id>\d+)/$', 'consultations.views.choose_panel'),
    url(r'^tutor/(?P<tutor_id>\d+)/$', 'consultations.views.tutor_index'),
	url(r'^tutor/(?P<tutor_id>\d+)/edit/$', 'consultations.views.tutor_detail'),
    url(r'^tutor/(?P<tutor_id>\d+)/consultations_detail/$', 'consultations.views.consultations_detail'),
    url(r'^tutor/(?P<tutor_id>\d+)/infoboard/$', 'consultations.views.edit_infoboard'),
    url(r'^tutor/(?P<tutor_id>\d+)/consultations/edit/(?P<consultation_id>\d+)/$', 'consultations.views.edit_consultation'),
	url(r'^tutor/(?P<tutor_id>\d+)/consultations/delete/(?P<consultation_id>\d+)/$', 'consultations.views.delete_consultation'),
	url(r'^tutor/(?P<tutor_id>\d+)/consultations/add/$', 'consultations.views.add_consultation'),
	url(r'^tutor/(?P<tutor_id>\d+)/html_saving/$', 'consultations.views.export_html'),
	url(r'^assistant/(?P<user_id>\d+)/$', 'consultations.views.assistant_index'),
	url(r'^assistant/(?P<user_id>\d+)/adduser/$', 'consultations.views.assistant_adduser'),
	url(r'^assistant/(?P<user_id>\d+)/consultations_delete_confirm/$', 'consultations.views.assistant_consultations_delete_confirm'),
	url(r'^assistant/(?P<user_id>\d+)/consultations_delete/$', 'consultations.views.assistant_consultations_delete'),
	url(r'^assistant/(?P<user_id>\d+)/tutor/(?P<tutor_id>\d+)/edit/$', 'consultations.views.assistant_tutor_edit'),
	url(r'^assistant/(?P<user_id>\d+)/tutor/(?P<tutor_id>\d+)/delete/confirm/$', 'consultations.views.assistant_tutor_delete_confirm'),
	url(r'^assistant/(?P<user_id>\d+)/tutor/(?P<tutor_id>\d+)/delete/$', 'consultations.views.assistant_tutor_delete'),
	url(r'^assistant/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/list/$', 'consultations.views.assistant_consultation_list'),
	url(r'^assistant/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/add/$', 'consultations.views.assistant_consultation_add'),
	url(r'^assistant/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/edit/(?P<consultation_id>\d+)/$', 'consultations.views.assistant_consultation_edit'),
	url(r'^assistant/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/delete/confirm/(?P<consultation_id>\d+)/$', 'consultations.views.assistant_consultation_delete_confirm'),
	url(r'^assistant/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/delete/(?P<consultation_id>\d+)/$', 'consultations.views.assistant_consultation_delete'),
	url(r'^assistant/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/deleteall/confirm/$', 'consultations.views.assistant_consultation_deleteall_confirm'),
	url(r'^assistant/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/deleteall/$', 'consultations.views.assistant_consultation_deleteall'),
	url(r'^assistant/(?P<user_id>\d+)/csvexport/$', 'consultations.views.assistant_export_csv'),
	url(r'^assistant/(?P<user_id>\d+)/backup/$', 'consultations.views.assistant_backup'),
	url(r'^assistant/(?P<user_id>\d+)/restore/$', 'consultations.views.assistant_restore'),
	url(r'^assistant/(?P<user_id>\d+)/export/$', 'consultations.views.export_csv'),
	url(r'^admin/(?P<user_id>\d+)/$', 'consultations.views.admin_index'),
	url(r'^admin/(?P<user_id>\d+)/choosepanel/$', 'consultations.views.admin_choose_panel'),
	url(r'^admin/(?P<user_id>\d+)/adduser/$', 'consultations.views.admin_adduser'),
	url(r'^admin/(?P<user_id>\d+)/consultations_delete_confirm/$', 'consultations.views.admin_consultations_delete_confirm'),
	url(r'^admin/(?P<user_id>\d+)/consultations_delete/$', 'consultations.views.admin_consultations_delete'),
	url(r'^admin/(?P<user_id>\d+)/tutor/(?P<tutor_id>\d+)/edit/$', 'consultations.views.admin_tutor_edit'),
	url(r'^admin/(?P<user_id>\d+)/tutor/(?P<tutor_id>\d+)/delete/confirm/$', 'consultations.views.admin_tutor_delete_confirm'),
	url(r'^admin/(?P<user_id>\d+)/tutor/(?P<tutor_id>\d+)/delete/$', 'consultations.views.admin_tutor_delete'),
	url(r'^admin/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/list/$', 'consultations.views.admin_consultation_list'),
	url(r'^admin/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/add/$', 'consultations.views.admin_consultation_add'),
	url(r'^admin/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/edit/(?P<consultation_id>\d+)/$', 'consultations.views.admin_consultation_edit'),
	url(r'^admin/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/delete/confirm/(?P<consultation_id>\d+)/$', 'consultations.views.admin_consultation_delete_confirm'),
	url(r'^admin/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/delete/(?P<consultation_id>\d+)/$', 'consultations.views.admin_consultation_delete'),
	url(r'^admin/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/deleteall/confirm/$', 'consultations.views.admin_consultation_deleteall_confirm'),
	url(r'^admin/(?P<user_id>\d+)/consultation/(?P<tutor_id>\d+)/deleteall/$', 'consultations.views.admin_consultation_deleteall'),
	url(r'^admin/(?P<user_id>\d+)/csvexport/$', 'consultations.views.admin_export_csv_confirm'),
	url(r'^admin/(?P<user_id>\d+)/backup/$', 'consultations.views.admin_backup'),
	url(r'^admin/(?P<user_id>\d+)/restore/$', 'consultations.views.admin_restore'),
	url(r'^admin/(?P<user_id>\d+)/export/$', 'consultations.views.admin_export_csv'),
	url(r'^admin/(?P<user_id>\d+)/assistants/$', 'consultations.views.admin_assistant_list'),
	url(r'^admin/(?P<user_id>\d+)/addassistant/$', 'consultations.views.admin_assistant_add'),
	url(r'^admin/(?P<user_id>\d+)/assistant/(?P<assistant_id>\d+)/delete/confirm/$', 'consultations.views.admin_assistant_delete_confirm'),
	url(r'^admin/(?P<user_id>\d+)/assistant/(?P<assistant_id>\d+)/delete/$', 'consultations.views.admin_assistant_delete'),
	url(r'^admin/(?P<user_id>\d+)/admins/$', 'consultations.views.admin_admin_list'),
	url(r'^admin/(?P<user_id>\d+)/admin/add/$', 'consultations.views.admin_admin_add'),
	url(r'^admin/(?P<user_id>\d+)/admin/(?P<admin_id>\d+)/delete/confirm/$', 'consultations.views.admin_admin_delete_confirm'),
	url(r'^admin/(?P<user_id>\d+)/admin/(?P<admin_id>\d+)/delete/$', 'consultations.views.admin_admin_delete'),
	url(r'^logout/$', 'consultations.views.logout'),
	
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
)
