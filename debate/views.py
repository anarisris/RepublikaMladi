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
These are the views that control the debates.
"""

import json
import datetime

# Generic class-based views
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

# Decorators. the first is a wrapper to convert function-based decorators
# to method decorators that can be put in subclass methods.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

# Response types
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect

# Some extras
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.template import RequestContext
from django.forms.formsets import formset_factory, BaseFormSet
from django.core.exceptions import ObjectDoesNotExist

# Application models
from republika.debate.models import *
from republika.debate.forms import UpdateNoteForm, \
    NoteForm, UpdateNotePosition

#Republika mladi additions
from django.contrib.comments import *
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.comments.forms import CommentForm
from django.db import connection

def get_debates(request):

    """
    Get all debates and serve them through JSON.
    """
    data = [debate.title for debate in Debate.objects.all().order_by('title')]
    return render_to_response(json.dumps(data), content_type='application/json')


def create_note(request):

    """
    This function creates a new note inside the debate board. It receives the order
    from the createNote() AJAX function. To create the note first we create the note
    in the DB, and if successful we return some of its parameters to the debate
    board for the user. In case the petition had errors, we return the error message
    that will be shown by jsnotify.

    .. versionadded:: 0.1.5
    """
    note_form = NoteForm(request.POST or None)
        
    if request.method == "POST" and request.is_ajax:        
        if note_form.is_valid():
            note_form_uncommited = note_form.save(commit=False)
            note_form_uncommited.author = request.user
            note_form_uncommited.debate = get_object_or_404(Debate,
                                                            pk=request.POST['debateid'])
            note_form_uncommited.title = request.POST['title']
            note_form_uncommited.message = request.POST['message']
            note_form_uncommited.column = get_object_or_404(Column,
                                                            pk=request.POST['column'])
            note_form_uncommited.row = get_object_or_404(Row, pk=request.POST['row'])
            note_form_uncommited.save()

             
            response_data = {}
            response_data['id'] = note_form_uncommited.id
            response_data['message'] = note_form_uncommited.message
            response_data['title'] = note_form_uncommited.title
            return HttpResponse(json.dumps(response_data), mimetype="application/json")

        else:
            msg = "The note form didn't validate. This fields gave errors: " \
            + str(note_form.errors)
    else:
        msg = "The petition was not POST."
        
    return HttpResponse(json.dumps(msg), mimetype="application/json")


def update_note(request):

    """
    Updated the current note with the POST data. UpdateNoteForm is an incomplete
    form that doesn't handle some properties, only the important for the note editing.
    """

    if request.method == "GET" and request.is_ajax:
        note = get_object_or_404(Note, pk=request.GET['noteid'])
        ctype = ContentType.objects.get_for_model(Note)
        latest_comments = Comment.objects.filter(is_public=True, is_removed=False, content_type=ctype, object_pk=note.id).order_by('submit_date')
        note.comment_count = Comment.objects.filter(is_public=True, is_removed=False, content_type=ctype, object_pk=note.id).count()
        note.save()
        form = CommentForm(target_object = note)

        response_data = {}
        response_data['author'] = {
		'name': note.author.username
	}
        response_data['debate'] = {
                'id': note.debate.pk
        }
        response_data['title'] = note.title
        response_data['message'] = note.message
        response_data['comments'] = [ 
	    {'username': c.user.username, 'comment': c.comment, 'submit_date': c.submit_date} for c in latest_comments]
        response_data["form_html"] = form.as_p()
        return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), mimetype="application/json")

    if request.method == "POST" and request.is_ajax:
        note = get_object_or_404(Note, pk=request.POST['noteid'])
        note_form = UpdateNoteForm(request.POST or None, instance=note)
        if note_form.is_valid():
            note_form_uncommited = note_form.save(commit=False)
            note_form_uncommited.title = request.POST['title']
            note_form_uncommited.message = request.POST['message']
            note_form_uncommited.last_mod_author = request.user

        
            note_form_uncommited.save()
            msg = "The note has been updated."
        else:
            msg = "The form is not valid, check field(s): " + note_form.errors
    else:
        msg = "There was some error in the petition."
        
    return HttpResponse(msg)

def update_position(request):

    """
    This view saves the new note position in the debate board. Instead of reloading
    all the note form with all the data, we use the partial form "UpdateNotePosition"
    which only handles the column and row of the note.
    """
    note = get_object_or_404(Note, pk=request.POST['noteid'])
    position_form = UpdateNotePosition(request.POST or None, instance=note)

    if request.method == "POST" and request.is_ajax:
        if position_form.is_valid():
            position_form_uncommited = position_form.save(commit=False)
            position_form_uncommited.column = get_object_or_404(Column, pk=request.POST['column'])
            position_form_uncommited.row = get_object_or_404(Row, pk=request.POST['row'])

            position_form_uncommited.save()
            msg = "The note has been updated."
        else:
            msg = "There has been an error validating the form."
    else:
        msg = "There was some error in the petition."

    return HttpResponse(msg)


def delete_note(request):
        

    """
    Deletes a note object.
    """
    note = get_object_or_404(Note, pk=request.POST['noteid'])

    if note.author == request.user or request.user.is_staff:
        ctype = ContentType.objects.get_for_model(Note)
        all_comments = Comment.objects.filter(is_public=True, is_removed=False, content_type=ctype, object_pk=note.id).all()
        for i in range(all_comments.count()):
            all_comments[i].delete()
        note.delete()
        return HttpResponse("The note has been deleted.")

    else:
        return HttpResponse("You're not the author of the note. Can't delete.")

def userprofile(request):

    ctype = ContentType.objects.get_for_model(Note)
    all_comments = Comment.objects.filter(is_public=True, is_removed=False, content_type=ctype, user=request.user).all()
    all_notes = Note.objects.filter(author=request.user)
    user = request.user
    return render_to_response('userprofile.html', {'all_comments':all_comments,
                                                   'all_notes':all_notes,
                                                   'user':user},)
class ViewDebate(DetailView):
    """
    View a debate.
    
    :context: get_place, notes, columns, rows
    """
    context_object_name = 'debate'
    template_name = 'debate/debate_view.html'

    def get_object(self):
        debate = get_object_or_404(Debate, pk=self.kwargs['debate_id'])
        
        # Check debate dates
        if datetime.date.today() >= debate.end_date or datetime.date.today() <  debate.start_date:
            self.template_name = 'debate/debate_outdated.html'
            #return Debate.objects.none()
        
        return debate

    def get_context_data(self, **kwargs):
        
        context = super(ViewDebate, self).get_context_data(**kwargs)
        columns = Column.objects.all().filter(debate=self.kwargs['debate_id'])
        rows = Row.objects.all().filter(debate=self.kwargs['debate_id'])
        current_debate = get_object_or_404(Debate, pk=self.kwargs['debate_id'])
        sort_by = self.request.GET.get('sort', '-comment_count')
        sort_by = self.request.GET.get('sort', '-rating_score')
        sort_by = self.request.GET.get('sort', '-date')
        notes = Note.objects.all().filter(debate=current_debate.pk).order_by(sort_by)

        try:
            last_note = Note.objects.latest('id')
        except:
            last_note = 0

        context['notes'] = notes
        context['columns'] = columns
        context['rows'] = rows
        if last_note == 0:
            context['lastnote'] = 0
        else:
            context['lastnote'] = last_note.pk

        return context


class ListDebates(ListView):
    """
    Return a list of debates for the current space.
    
    :context: get_place
    """
    paginate_by = 10

    def get_queryset(self):
        debates = Debate.objects.all()

        # Here must go a validation so a user registered to the space
        # can always see the debate list. While an anonymous or not
        # registered user can't see anything unless the space is public

        return debates
