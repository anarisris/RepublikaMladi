from django.contrib import admin
from republika.debate.models import *

class ColumnInline(admin.TabularInline):

    model = Column
    extra = 1

class RowInline(admin.TabularInline):

    model = Row
    extra = 1

class DebateAdmin(admin.ModelAdmin):

    list_display = ('title', 'date')
    inlines = [ColumnInline, RowInline]

class NoteAdmin(admin.ModelAdmin):

    list_display = ('title', 'message', 'author', 'date')

admin.site.register(Debate, DebateAdmin)
admin.site.register(Note, NoteAdmin)
