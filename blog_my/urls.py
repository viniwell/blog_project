from django.urls import path
from . import views


app_name = 'blog_my'

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('my_products/', views.post_list, name='post_list'),
    path('detail/<slug:post>/', views.post_detail, name='post_detail'),
    path('add_advertisement/', views.add_advertisement, name='add_advertisement'),
    path('<int:post_id>/post_comment/', views.post_comment, name='post_comment'),
    
    path('register/', views.register, name='register'),
]