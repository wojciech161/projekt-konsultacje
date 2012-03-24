from django.conf.urls.defaults import patterns, include, url
from konsultacje import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'konsultacje.views.home', name='home'),
    # url(r'^konsultacje/', include('konsultacje.foo.urls')),
    url(r'^consultations/$', 'consultations.views.consultation_index'),
    url(r'^consultations/(?P<consultation_id>\d+)/$', 'consultations.views.consultation_detail'),
    url(r'^tutors/$', 'consultations.views.tutors_index'),
    url(r'^tutor/(?P<tutor_id>\d+)/$', 'consultations.views.tutor_index'),
    url(r'^tutor/(?P<tutor_id>\d+)/edit/$', 'consultations.views.tutor_detail'),
    url(r'^tutor/(?P<tutor_id>\d+)/consultations/$', 'consultations.views.tutor_consultations'),
    url(r'^tutor/(?P<tutor_id>\d+)/consultations/edit/(?P<consultation_id>\d+)/$', 'consultations.views.edit_consultation'),
    url(r'^authorization/$', 'consultations.views.authorization'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
)
