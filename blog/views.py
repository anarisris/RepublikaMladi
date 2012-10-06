from django.shortcuts import render_to_response, render
from republika.blog.models import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404
import datetime
from datetime import date
rom_months = ['', '', '', '', '', '', '', '', '', '', '', '']

def list(request, archive=1):
    if archive == "1":
        return HttpResponseRedirect("/")
    page = (int(archive)*7)
    if Post.objects.all().count > page+7:
        posts = Post.objects.order_by('-published')[page-7:page]
    else:
        posts = Post.objects.order_by('-published')[page-7:page]
    if Post.objects.all().count() > page:
        next = (int(archive))+1
    else:
        next = 0
    previous = (int(archive))-1

    arch = Post.objects.dates('published', 'month', order='DESC')

    archives = {}

    for i in arch:
        year = i.year
        month = i.month
        try:
            archives[year][month-1][1]=True
        except KeyError:
            k = 0
            # catch the KeyError, and set up list for that year
            archives[year]=[[date(year,k+1,1), False, rom] for k, rom in enumerate(rom_months)]
            archives[year][month-1][1]=True

    return render_to_response('blog/list.html', {'posts':posts,
                                            'next':next,
                                            'previous':previous,
                                            'categories':Category.objects.all(),
                                            'tags':Tags.objects.all(),
                                            'latest':Post.objects.latest('published'),
                                            'archives':sorted(archives.items(),reverse=True),
                                            'archive':archive,
                                            },)

def detail(request, slug):
    try:
        post = Post.objects.filter(slug=slug)[0]
        try:
            previous_post = post.get_previous_by_published()
        except:
            previous_post = ""
        try:
            next_post = post.get_next_by_published()
        except:
            next_post = ""
    except:
        next_post = ""
        previous_post = ""
        post = ""
    return render_to_response('blog/detail.html', {'post':post,
                                                  'next_post':next_post,
                                                  'previous_post':previous_post,
                                                  'categories':Category.objects.all(),
                                                  'tags':Tags.objects.all(),

                                                 },)

def month(request, year, month):
    date = datetime.datetime(int(year), int(month),1)
    try:
        posts = Post.objects.order_by('-published').filter(published__year=year).filter(published__month=month)
    except:
        posts = ""
    return render_to_response('blog/month.html', {'posts':posts,
                                            'date':date,
                                            },)

def year(request, year):
    post_error = ""
    year = int(year)
    yr = datetime.datetime(year, 1,1)
    months=12
    by_month=[]
    if Post.objects.filter(published__year=year).count():
        if year == datetime.datetime.now().year:
            months = datetime.datetime.now().month
        if month in range(1, months+1):
            by_month.append({datetime.datetime(year,month, 1):

    Post.objects.filter(published__month=month).filter(published__year=year)})
    elif year > datetime.datetime.now().year:
        post_error = "It is not yet %d, try and earlier year." %year 
    else:
        post_error = "There are no posts for %d." %year
    return render_to_response('blog/year.html', {'by_month':by_month,
                                            'yr':yr,
                                            'post_error':post_error,
                                            },)

def category(request):
  return render_to_response('blog/category.html', { 'categories':Category.objects.all(),},)

def one_category(request, category):
    posts = Post.objects.order_by('-published').filter(categories__name=category.lower())
    return render_to_response('blog/one_category.html', {'posts':posts,
                                            'category':category,
                                            },)

def tags(request):
    return render_to_response('blog/one_category.html', {'tags':Tags.objects.all(),},)

def one_tag(request, tag):
    posts = Post.objects.order_by('-published').filter(tags__name=tag.lower())
    return render_to_response('blog/one_tag.html', {'posts':posts,
                                            'tag':tag,
                                            },)
