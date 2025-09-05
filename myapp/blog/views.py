from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse


# Create your views here.
def index(request):
    blog_title ="Latest Posts"
    posts = [
        {'id':1,'title':'Post 1', 'content':'content of Post 1'},
        {'id':2,'title':'Post 2', 'content':'content of Post 2'},
        {'id':3,'title':'Post 3', 'content':'content of Post 3'},
        {'id':4,'title':'Post 4', 'content':'content of Post 4'}
    ]
    return render(request, "blog/index.html",{'blog_title': blog_title, 'posts': posts})

def detail(request, post_id):
     return render(request, "blog/detail.html")

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))

def new_url_view(request):
    return HttpResponse("this is the new URL")