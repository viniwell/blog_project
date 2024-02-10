from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ShopPostForm, CommentForm, RegisterForm, LoginForm
from .models import Shop_Post, Profile
from django.views.decorators.http import require_POST
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from functools import partial

def checkUser(request, func):
    try:
        request.user.profile
        return False
    except:
        return register(request, func)


def mainpage(request):
    posts=Shop_Post.published.all().order_by('-publish')
    return render(request, 'blog_my/post/mainpage.html', {'posts':posts})

def register(request:HttpRequest, to=None):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            profile=Profile(user=new_user)
            new_user.save()
            profile.save()
            login(request, new_user)
            if to:
                return to()
            else:
                return mainpage(request)
    else:
        form=RegisterForm()
    return render(request, 'blog_my/post/register.html', {'form':form})

def userLogin(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        cd=form.cleaned_data
        user=authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)

    return mainpage(request)

def post_list(request):
    post_list = Shop_Post.published.all()
    paginator=Paginator(post_list, 3)
    page_number=request.GET.get('page', 1)
    try:
        posts=paginator.page(page_number)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts=paginator.page(1)
    return render(request, 'blog_my/post/list.html', {'posts': posts})


def post_detail(request, post):
    posts = get_object_or_404(Shop_Post, slug=post, status=Shop_Post.Status.PUBLISHED)
    
    comments=posts.comments.filter(active=True)

    form=CommentForm()

    return render(request, 'blog_my/post/detail.html', 
                  {'post': posts, "comments":comments, 'form':form})

def add_advertisement(request):
    c=checkUser(request, partial(add_advertisement, request))
    if c:
        return c
    sent=False
    post=None
    if request.method=='POST':
        form=ShopPostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.slug=''.join(letter for letter in post.title+str(post.publish) if letter not in '~`!@#$%^*(){}[]|"/?><=+-:; &.,')
            post.author=request.user
            post.save()
            sent=True
    else:
        form=ShopPostForm()
    return render(request, 'blog_my/post/add_advertisement.html', {
        'form':form,
        'post':post,
        'sent':sent,
    })

@require_POST
def post_comment(request, post_id):
    post=get_object_or_404(Shop_Post, id=post_id, status=Shop_Post.Status.PUBLISHED)
    c=checkUser(request, partial(post_detail, request, post))
    if c:
        return c
    comment=None
    #Коментар було відправлено
    form=CommentForm(data=request.POST)
    if form.is_valid():
        #створити комент не зберігаючи у базі даних
        comment=form.save(commit=False)
        comment.post=post
        comment.save()
    return render(request, 'blog_my/post/comment.html', context={
        'post':post,
        'form':form,
        'comment':comment,
    })