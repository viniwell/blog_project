from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ShopPostForm, CommentForm
from .models import Shop_Post
from django.views.decorators.http import require_POST


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