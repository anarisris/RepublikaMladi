from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings
from republika.core.views import *

urlpatterns = patterns('',
   	(r'^$', contact),
    	(r'^newdebate/$', contactDebate),
        (r'newdocument/$', contactDocument),
)

