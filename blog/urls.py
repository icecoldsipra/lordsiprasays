from django.urls import path
from .views import (
    blog_home, user_posts, post_create, post_detail, post_update, user_comments,
    about_page, contact_admin
)

urlpatterns = [
    path('', blog_home, name='blog-home'),
    path('posts/', user_posts, name='blog-posts'),
    path('posts/create/', post_create, name='blog-create'),
    path('posts/<slug:slug>/', post_detail, name='blog-detail'),
    path('posts/<slug:slug>/update/', post_update, name='blog-update'),
    path('comments/', user_comments, name='blog-comments'),
    path('about/', about_page, name='blog-about'),
    path('contact/', contact_admin, name='blog-contact'),
]
