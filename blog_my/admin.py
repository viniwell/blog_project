from django.contrib import admin

from .models import Shop_Post, Size, Comment, Profile

from django.contrib.auth.models import User



@admin.register(Shop_Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('publish','title', 'size',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(Size)
class PostAdmin(admin.ModelAdmin):
    list_display = ['size']
    list_filter = ['size']
    search_fields = ['size']
    prepopulated_fields = {'slug': ('size',)}
    ordering = ['size']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'post', 'name', 'email']
    search_fields = ['name', 'email', 'post', 'created', 'active']
    date_hierarchy = 'created'
    ordering = ['created']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user', 'birthday', 'photo']
    list_filter=['user', 'birthday', 'photo']
    search_field=['user', 'birthday']
    ordering=['user']