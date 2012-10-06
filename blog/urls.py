from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from republika.blog.views import *
urlpatterns = patterns('',
        (r'^$', list),
        (r'^archive/(\d{1,2})/$', list),
        (r'^(?P<month>\d{1,2})/(?P<year>\d{4})/$', month),
        (r'^([0-9]{4}/\d{1,2})/(?P<slug>.*)/$', detail),
        (r'^(?P<year>\d{4})/$', year),
        (r'^category/$', category),
        (r'^category/(?P<category>.*)/$', one_category),
        (r'^tag/$', tags),
        (r'^tag/(?P<tag>.*)/$', one_tag),
        )
