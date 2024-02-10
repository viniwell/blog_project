from typing import Any
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.files.images import ImageFile
import datetime

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Shop_Post.Status.PUBLISHED)


class Shop_Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=True)
    body = models.TextField()
    size=models.ForeignKey("Size", verbose_name=("Одяг"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_posts')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog_my:post_detail", args=[self.slug])

    

class Size(models.Model):
    size=models.CharField(max_length=3)
    slug = models.SlugField(max_length=3, null=True)

    class Meta:
        ordering = ['size']

    def __str__(self):
        return self.size

class Comment(models.Model):
    post=models.ForeignKey(Shop_Post, on_delete=models.CASCADE, related_name='comments')
    name=models.CharField(max_length=80)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=['created']
        indexes=[
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    birthday=models.DateField(blank=True, null=True)
    bio=models.CharField(max_length=150, blank=True)
    photo=models.ImageField(upload_to='users/%Y%m%d', blank=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        date=datetime.datetime.now()
        self.setup(bio='No bio yet.', photo='media/anonymous/anonymoususer.png', birthday={'year':date.year, 'month':date.month, 'day':date.day})

    def setup(self, bio=None, photo=None, birthday=None):
        if bio:
            self.__setattr__('bio', bio)
        if photo:
            image=ImageFile(open(photo, 'rb'))
            self.__setattr__('photo', image)
        if birthday:
            self.__setattr__('birthday', datetime.date(year=birthday['year'], month=birthday['month'], day=birthday['day']))