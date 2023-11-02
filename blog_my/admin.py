from django.contrib import admin

from .models import Shop_Post, Size



@admin.register(Shop_Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
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