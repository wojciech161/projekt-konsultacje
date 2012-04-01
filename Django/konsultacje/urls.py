from django.conf.urls.defaults import patterns, include, url
from konsultacje import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'consultations.views.consultation_index'),
	url(r'^authorization/$', 'consultations.views.authorization'),
    url(r'^tutor/(?P<tutor_id>\d+)/$', 'consultations.views.tutor_index'),
	url(r'^tutor/(?P<tutor_id>\d+)/edit/$', 'consultations.views.tutor_detail'),
    url(r'^tutor/(?P<tutor_id>\d+)/consultations_detail/$', 'consultations.views.consultations_detail'),
    url(r'^tutor/(?P<tutor_id>\d+)/infoboard/$', 'consultations.views.edit_infoboard'),
    url(r'^tutor/(?P<tutor_id>\d+)/consultations/edit/(?P<consultation_id>\d+)/$', 'consultations.views.edit_consultation'),
	url(r'^tutor/(?P<tutor_id>\d+)/consultations/delete/(?P<consultation_id>\d+)/$', 'consultations.views.delete_consultation'),
	url(r'^tutor/(?P<tutor_id>\d+)/consultations/add/$', 'consultations.views.add_consultation'),
	url(r'^logout/$', 'consultations.views.logout'),
	
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
)
