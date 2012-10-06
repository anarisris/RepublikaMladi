# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2012 Cidadania S. Coop. Galega
#
# This file is part of e-cidadania.
#
# e-cidadania is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# e-cidadania is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with e-cidadania. If not, see <http://www.gnu.org/licenses/>.

"""  
This file contains all the URLs that e_cidadania will inherit when the user
access to '/spaces/'.
"""
from django.conf.urls import *
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import *
from republika.debate.views import ListDebates, ViewDebate
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template

from republika.debate.models import Note
from djangoratings.views import AddRatingFromModel

urlpatterns = patterns('republika.debate.views',

    url(r'rate-my-post/(?P<object_id>\d+)/(?P<score>\d+)/', AddRatingFromModel(), {
        'app_label': 'debate',
        'model': 'note',
        'field_name': 'rating',
    }),

    url(r'^$', ListDebates.as_view(), name='list-debates'),

    url(r'^(?P<debate_id>\d+)/', ViewDebate.as_view(), name='view-debate'),
    
    url(_(r'^update_position/'), 'update_position', name='update-note-position'),
    
    url(_(r'^update_note/'), 'update_note', name='update-note'),
    url(_(r'^update_note_single/'), 'update_note', name='update_note_single'),
    
    url(_(r'^create_note/'), 'create_note', name='create-note'),
    
    url(_(r'^delete_note/'), 'delete_note', name='delete-note'),
    url(_(r'login_popup/'), direct_to_template, {
        'template': 'debate/login.html'
    }),
    url(_(r'^(?P<debate_id>\d+)?sort=<?P<sort>votes_count'), ViewDebate.as_view(), name='votes-count'),
    url(_(r'^(?P<debate_id>\d+)/comment_count/'), ViewDebate.as_view( context_object_name = "debate", template_name="/debate/comment_count.html"), name='comment-count'),
    url(_(r'^(?P<debate_id>\d+)/date/'), ViewDebate.as_view( context_object_name = "debate", template_name="/debate/date.html"), name='date'),
    url(_(r'^userprofile/$'), 'userprofile', name='userprofile'),    
    


    # Editing debates is not allowed at this time
   # (r'^(?P<debate_id>\d+)', 'edit_debate'),
    
   # (r'^(?P<debate_id>\d+)', 'delete_debate'),

)
