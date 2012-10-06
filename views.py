from republika.blog.models import Post
from django.template import RequestContext

def xd_receiver(request):
    return render_to_response('xd_receiver.html')

def footer(request):
    return {'posts_latest':Post.objects.order_by('-published')[:3],}


