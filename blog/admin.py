from django.contrib import admin
from republika.blog.models import *

class PostAdmin(admin.ModelAdmin):
    filter_horizontal=('tags',)
    list_display=('title', 'published')
    prepopulated_fields={'slug': ('title',),}

admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Post, PostAdmin)
