from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse ,Http404
from django.urls import reverse
import logging 
from .models import Category, post, AboutUs
from django.core.paginator import Paginator
from .forms import ForgotPasswordForm, LoginForm, PostForm, ResetPasswordForm, contactForm,RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group
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

    all_posts = post.objects.filter(is_published = True)

    #paginator
    paginator1 = Paginator(all_posts, 5)
    page_number = request.GET.get("page")
    page_object = paginator1.get_page(page_number)

    return render(request, "blog/index.html",{'blog_title': blog_title, 'page_obj': page_object})

def detail(request, slug):
    if request.user and not request.user.has_perm('blog.view_post'):
        # if user logged in and user don't have permission on view_post its redirect
        messages.error(request, 'You dont have a permmission to view any post')
        return redirect('blog:index')

     #static data
     # post = next((item for item in posts if item['id']== int(post_id)),None)
    try:
        # getting data from model by post id
        post1 = post.objects.get(slug = slug)
        related_posts = post.objects.filter(category = post1.category).exclude(pk = post1.id)

    except post.DoesNotExist:
        raise Http404("post doesn't exit!")

        #  logger = logging.getLogger("TESTING")
        #  logger.debug(f'post variables is {post} ')
 
    return render(request, "blog/detail.html",{'post': post1, 'related_posts': related_posts})

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))
 
def new_url_view(request):
    return HttpResponse("this is the new URL")

def contact(request):
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


def about(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "default content goes here" #default text
    else:
        about_content = about_content.content
    return render(request, "blog/about.html",{'about_contents': about_content})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # user data created
            user.set_password(form.cleaned_data['password'])
            user.save()
            #add user to readers groups
            readers_group,created = Group.objects.get_or_create(name="Readers")
            user.groups.add(readers_group)
            messages.success(request,'registration successfull, you can log in ')
            return redirect('blog:login')
            
    
    return render(request, "blog/register.html",{'form':form})


def login(request):
    form = LoginForm() 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username =form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print ("login success")
                return redirect('blog:dashboard') #redirect to dashboard


    return render(request, "blog/login.html",{'form': form })


def dashboard(request):
    blog_title = "MY Posts"
    #getting user posts data
    all_posts = post.objects.filter(user=request.user)

    #paginator
    paginator1 = Paginator(all_posts, 5)
    page_number = request.GET.get("page")
    page_object = paginator1.get_page(page_number)

    return render(request, "blog/dashboard.html",{'blog_title':blog_title, 'page_obj':page_object})

def logout(request):
    auth_logout(request)
    return redirect('blog:index')


def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        #form
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            #send email to reset password
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "Reset Password Requested"
            message = render_to_string('blog/reset_password_email.html', {
                'domain': domain,
                'uid': uid,
                'token': token
            })

            send_mail(subject, message, 'noreply@jvlcode.com', [email])
            messages.success(request, 'Email has been sent')
    return render(request, "blog/forgot_password.html",{'form':form})

def reset_password(request, uidb64, token):
    form =  ResetPasswordForm()
    #form
    if request.method == 'POST':
       form =  ResetPasswordForm(request.POST)
       if form.is_valid():
           new_password = form.cleaned_data['new_password']
           try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)

           except(ValueError,TypeError,OverflowError,User.DoesNotExist):
               user = None

           if user is not None and default_token_generator.check_token(user, token):
               user.set_password(new_password)
               user.save()
               messages.success(request,'Your password has been reset successfuly')
               return redirect('blog:login')
           else:
               messages.error(request, 'The password link is invalid')
               
       
    return render(request, "blog/reset_password.html",{'form':form})

@login_required
@permission_required('blog.add_post' , raise_exception=True)
def new_post(request):
    form = PostForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        #form
        form = PostForm(request.POST , request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:dashboard')
        
    return render(request, "blog/new_post.html",{'categories':categories, 'form':form})

@login_required
@permission_required('blog.change_post' ,raise_exception=True)
def edit_post(request, post_id):
    form = PostForm()
    categories = Category.objects.all()
    Post = get_object_or_404(post , id=post_id)
    if request.method =='POST':
        #form
        form = PostForm(request.POST , request.FILES, instance=Post)
        if form.is_valid():
            form.save()
            messages.success(request,'Post updated successfuly')
            return redirect('blog:dashboard')

    return render(request, "blog/edit_post.html" ,{'categories':categories , 'post':Post , 'form':form})
@login_required
@permission_required('blog.delete_post' ,raise_exception=True)
def delete_post(request, post_id):
    Post = get_object_or_404(post ,id=post_id)
    Post.delete()
    messages.success(request,'Post deleted successfuly')
    return redirect('blog:dashboard')
@login_required
@permission_required('blog.can_publish' ,raise_exception=True)
def publish_post(request, post_id):
    Post = get_object_or_404(post ,id=post_id)
    Post.is_published = True
    Post.save()
    messages.success(request,'Post published successfuly')
    return redirect('blog:dashboard')