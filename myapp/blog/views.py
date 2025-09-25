from django.shortcuts import render,redirect
from django.http import HttpResponse ,Http404
from django.urls import reverse
import logging 
from .models import post

# Static demo data
# posts = [
#         {'id':1,'title':'Post 1', 'content':'content of Post 1'},
#         {'id':2,'title':'Post 2', 'content':'content of Post 2'},
#         {'id':3,'title':'Post 3', 'content':'content of Post 3'},
#         {'id':4,'title':'Post 4', 'content':'content of Post 4'}
#     ]

# Create your views here.
def index(request):
    blog_title ="Latest Posts"
    # getting data from post model
    posts = post.objects.all()
    return render(request, "blog/index.html",{'blog_title': blog_title, 'posts': posts})

def detail(request, slug):
     #static data
     # post = next((item for item in posts if item['id']== int(post_id)),None)
    try:
        # getting data from model by post id
        post1 = post.objects.get(slug = slug) 

    except post.DoesNotExist:
        raise Http404("post doesn't exit!")

        #  logger = logging.getLogger("TESTING")
        #  logger.debug(f'post variables is {post} ')

    return render(request, "blog/detail.html",{'post': post1})

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))
 
def new_url_view(request):
    return HttpResponse("this is the new URL")