# coding=utf-8
from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from djangoratings.fields import RatingField

class Debate(models.Model):

    """
    Debate object. In every space there can be unlimited debates, each one of
    them holds all the related notes. Debates are filtered by space. Start/End
    dates are for letting users use the debate or not.
    versionadded:: 0.1b
    """

    title = models.CharField(_('Title'), max_length=200, unique=True)
    description = models.TextField(_('Desctiption'), blank=True, null=True)
    scope = models.CharField(_('Scope'), blank=True, null=True, max_length=100)
    video = models.URLField(_('Youtube embed link'), blank=True, null=True)
    date = models.DateTimeField(_('Created on'), auto_now_add=True)
    author = models.ForeignKey(User, blank=True, null=True)
    date_mod = models.DateTimeField(_('Last modified'), auto_now=True)
    start_date = models.DateField(_('Start date '), blank=True, null=True)
    end_date = models.DateField(_('End date'), blank=True, null=True)
    image = models.ImageField(upload_to='images/')


    def __unicode__(self):
        if self.title is None:
            return "None"
        else:
            return self.title

    def is_active(self):
        if datetime.date.today() >= self.end_date or datetime.date.today() <= self.start.date:
            return False
        else:
            return True

    @models.permalink
    def get_absolute_url(self):
        return ('view-debate', (), {
                'debate_id': str(self.id)})

class Column(models.Model):
    
    criteria = models.CharField(_('Prashanje'), max_length=1000, blank=True, null=True)
    debate = models.ForeignKey(Debate, blank=True, null=True)

    def __unicode__(self):
        return self.criteria

class Row(models.Model):

    criteria = models.CharField(_('Prashanje'), max_length=1000, blank=True, null=True)
    debate = models.ForeignKey(Debate, blank=True, null=True)

    def __unicode__(self):
        return self.criteria

class Note(models.Model):
    column = models.ForeignKey(Column, null=True, blank=True)
    row = models.ForeignKey(Row, null=True, blank=True)
    debate = models.ForeignKey(Debate, null=True, blank=True)
    title = models.CharField(_('Title'), max_length=60, blank=True, null=True)
    message = models.TextField(_('Message'), max_length=100, null=True, blank=True)

    author = models.ForeignKey(User, null=True, blank=True, related_name="note_author")
    last_mod_author = models.ForeignKey(User, null=True, blank=True, related_name="update_author")
    date = models.DateTimeField(_('Created on'), auto_now_add=True)
    last_mod = models.DateTimeField(_('Last modified'), auto_now=True)
    rating = RatingField(range=3, can_change_vote = False, allow_anonymous = False, allow_delete = False, use_cookies = False)
    comment_count = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.message


