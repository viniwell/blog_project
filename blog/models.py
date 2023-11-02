from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT='DF', 'Draft'
        PUBLISHED='PB', 'Published'

    title= models.CharField(max_length=250)
    slug=models.SlugField(max_length=250, null=True)
    author=models.ForeignKey(User, on_delete=models.RESTRICT, related_name='blog_posts', null=True)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2,
                            choices=Status.choices,
                            default=Status.DRAFT)
    

    class Meta:
        ordering=['-publish']
        indexes=[
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title