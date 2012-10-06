from django import template
from republika.blog.models import *

register = template.Library()

@register.inclusion_tag('blog/category.html')
def categories_list():
    return { 'categories': Category.objects.all() }
