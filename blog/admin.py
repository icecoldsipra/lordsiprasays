from django.contrib import admin
from .models import Category, Post, Comment, Contact, PostViewCount


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['tag', 'pk', 'date_created']
    # list_filter = ['tag']
    # search_fields = ['tag']  # Add search bar in Admin panel
    readonly_fields = ['date_created']
    # prepopulated_fields = {'slug': ('title', )} # Automatically updates 'slug' field based on title
    ordering = ['tag']  # Sort in descending order


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'pk', 'slug', 'author', 'views', 'comments', 'is_live', 'image', 'date_created',
                    'date_posted', 'date_updated']
    list_filter = ['title', 'author', 'is_live']
    search_fields = ['title', 'author', 'is_live']  # Add search bar in Admin panel
    readonly_fields = ['author', 'views', 'comments', 'date_created', 'date_posted', 'date_updated']
    # prepopulated_fields = {'slug': ('title', )} # Automatically updates 'slug' field based on title
    ordering = ['-date_created']  # Sort in descending order


class PostViewCountAdmin(admin.ModelAdmin):
    list_display = ['ip', 'pk', 'country', 'city', 'post', 'timestamp']
    list_filter = []
    search_fields = ['post', 'ip', 'country', 'city']  # Add search bar in Admin panel
    readonly_fields = ['post', 'ip', 'country', 'city', 'timestamp']
    # prepopulated_fields = {'slug': ('title', )} # Automatically updates 'slug' field based on title
    ordering = ['-timestamp']  # Sort in descending order


class CommentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'pk', 'content', 'post', 'status', 'is_live', 'is_edited', 'date_created', 'date_updated',
                    'reviewed_by', 'review_time', 'review_notes']
    list_filter = ['owner', 'post', 'status', 'is_live', 'is_edited']
    search_fields = ['owner', 'post', 'is_live', 'is_edited']
    readonly_fields = ['owner', 'post', 'date_created', 'date_updated', 'reviewed_by', 'review_time']
    ordering = ['-date_created']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk', 'email', 'subject', 'message', 'timestamp']
    list_filter = ['subject']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostViewCount, PostViewCountAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contact, ContactAdmin)
