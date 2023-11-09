from django.shortcuts import render, get_object_or_404


from .models import Shop_Post


def post_list(request):
    posts = Shop_Post.published.all()
    return render(request, 'blog_my/post/list.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Shop_Post, id=id, status=Shop_Post.Status.PUBLISHED)
    
    return render(request, 'blog_my/post/detail.html', {'post': post})