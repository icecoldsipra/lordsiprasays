from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Comment
from django.shortcuts import get_object_or_404
