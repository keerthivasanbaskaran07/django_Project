from django.shortcuts import render,redirect
from django.http import HttpResponse ,Http404
from django.urls import reverse
import logging 
from .models import post, AboutUs
from django.core.paginator import Paginator
from .forms import contactForm

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

    all_posts = post.objects.all()

    #paginator
    paginator1 = Paginator(all_posts, 5)
    page_number = request.GET.get("page")
    page_object = paginator1.get_page(page_number)

    return render(request, "blog/index.html",{'blog_title': blog_title, 'page_obj': page_object})

def detail(request, slug):
     #static data
     # post = next((item for item in posts if item['id']== int(post_id)),None)
    try:
        # getting data from model by post id
        post1 = post.objects.get(slug = slug)
        related_posts = post.objects.filter(Category = post1.Category).exclude(pk = post1.id)

    except post.DoesNotExist:
        raise Http404("post doesn't exit!")

        #  logger = logging.getLogger("TESTING")
        #  logger.debug(f'post variables is {post} ')
 
    return render(request, "blog/detail.html",{'post': post1, 'related_posts': related_posts})

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))
 
def new_url_view(request):
    return HttpResponse("this is the new URL")

def contact_view(request):
    if request.method == 'POST': # submiting values arrived here
       form = contactForm(request.POST) # getting values in post page and sending to contact page
       name = request.POST.get('name') 
       email = request.POST.get('email')
       password = request.POST.get('password')
       logger = logging.getLogger("TESTING")
       if form.is_valid():
            logger.debug(f'POST Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            # send email or save in database 
            success_message = 'Your Email Has Been Send!'
            return render(request, "blog/contact.html" ,{'form':form, 'success_message': success_message})
       else:
            logger.debug('Form validation failure')
       return render(request, "blog/contact.html" ,{'form':form, 'name': name, 'email': email, 'password': password})     
    return render(request, "blog/contact.html")


def about_view(request):
    about_content = AboutUs.objects.first().content
    return render(request, "blog/about.html",{'about_contents': about_content})
