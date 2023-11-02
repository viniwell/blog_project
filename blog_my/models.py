from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone




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

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title
    

class Size(models.Model):
    size=models.CharField(max_length=3)
    slug = models.SlugField(max_length=3, null=True)

    class Meta:
        ordering = ['size']