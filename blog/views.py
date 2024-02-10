from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import Post, Comment
from taggit.models import Tag
from django.db.models import Count


class Post_list_view(ListView):
    """Алернативна post list"""
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=3
    template_name='blog/post/list.html'

def post_list(request, tag_slug=None):
    post_list=Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator=Paginator(post_list, 3)
    page_number=request.GET.get('page', 1)
    try:
        posts=paginator.page(page_number)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts=paginator.page(1)
    return render(request, 'blog/post/list.html', {'posts':posts,'tag':tag})


def post_detail(request, year, month, day, post):
    post=get_object_or_404(Post, slug=post, status=Post.Status.PUBLISHED,
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)
    #list of active comments
    comments=post.comments.filter(active=True)
    #form for commenting of users
    form=CommentForm()

    post_tags_id=post.tags.values_list('id', flat=True)
    similar=Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    #annotate by count of comments and order by this field
    similar=similar.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', 
                  {'post':post, "comments":comments, 'form':form, "similar":similar})

def post_share(request, post_id):
    post=get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent=False
    if request.method=='POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject=f'{cd["name"]} recommends you reading {post.title}'
            message=f'Read {post.title} at {post_url}\n\n' \
                    f'{cd["name"]}\'s comments: {cd["comments"]}'
            send_mail(subject, message, 'viniwell2807@gmail.com', [cd['to']])
            sent=True
    else:
        form=EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})


@require_POST
def post_comment(request, post_id):
    post=get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment=None
    #Коментар було відправлено
    form=CommentForm(data=request.POST)
    if form.is_valid():
        #створити комент не зберігаючи у базі даних
        comment=form.save(commit=False)
        comment.post=post
        comment.save()
    return render(request, 'blog/post/comment.html', context={
        'post':post,
        'form':form,
        'comment':comment,
    })
