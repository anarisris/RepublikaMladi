from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings 
from republika.views import *
from django.contrib import admin
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from republika.settings import STATIC_ROOT, MEDIA_ROOT
admin.autodiscover()
urlpatterns = patterns('',

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': STATIC_ROOT}),

    url(r'^admin/', include(admin.site.urls)),
    (r'^$', direct_to_template, {'template': 'index.html'}),
    (r'^page/$', direct_to_template, {'template': 'page.html'}),
    (r'^general/$', direct_to_template, {'template': 'general.html'}),
    (r'^core/', include('republika.core.urls')),
    (r'^inicijatori/$', direct_to_template, {'template': 'inicijatori.html'}),
    (r'^dokumenti/$', direct_to_template, {'template': 'dokumenti.html'}),
    (r'^infografik/$', direct_to_template, {'template': 'infografik.html'}),
    (r'^za-stranata/$', direct_to_template, {'template': 'za_stranata.html'}),
    (r'^index/$', direct_to_template, {'template': 'index.html'}),
    (r'^blog/', include('republika.blog.urls')),
    (r'^debate/', include('republika.debate.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^social/', include('socialregistration.urls',
                namespace = 'socialregistration')),
    (r'^logged-in/', direct_to_template, {'template': 'logged_in.html'}),
    (r'^thanks/', direct_to_template, {'template': 'thanks.html'}),
    (r'^xd_receiver/$', xd_receiver),
    (r'^dokumenti/domashno-zakonodavstvo/$', direct_to_template, {'template':'dokumenti/dokument_list_1.html'}),
    (r'^dokumenti/istrazuvanja/$', direct_to_template, {'template':'dokumenti/dokument_list_2.html'}),
    (r'^dokumenti/megjunarodni/$', direct_to_template, {'template':'dokumenti/dokument_list_3.html'}),
    (r'^dokumenti/standardi/$', direct_to_template, {'template':'dokumenti/dokument_list_4.html'}),
    (r'^dokumenti/priracnici/$', direct_to_template, {'template':'dokumenti/dokument_list_5.html'}),
    (r'^privatnost/$', direct_to_template, {'template': 'privatnost.html'}),
    (r'^odnesuvanje/$', direct_to_template, {'template': 'odnesuvanje.html'}),
    (r'^google04ff0a6e844d53ef.html/$', direct_to_template, {'template': 'google04ff0a6e844d53ef.html' }),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^networking-days/$', direct_to_template, {'template': 'networking_days.html' }),
)
