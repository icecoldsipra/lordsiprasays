from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, TrendingPost
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=Post)
def set_trending_post_flag(sender, instance, created, **kwargs):
    if created and instance.is_live:
        TrendingPost.objects.get_or_create(
            post=instance,
            is_new=True
        )
