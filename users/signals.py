from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import CustomUser, LoggedInUser
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from users.views import get_user_location


@receiver(pre_delete, sender=CustomUser)
def protect_superuser(sender, instance, **kwargs):
    """
    Prevent admin members from deleting superuser account
    """
    if instance.is_superuser:
        raise PermissionDenied


@receiver(user_logged_in)
def on_user_logged_in(sender, user, **kwargs):
    LoggedInUser.objects.get_or_create(user=user)


@receiver(user_logged_out)
def on_user_logged_out(sender, user, **kwargs):
    LoggedInUser.objects.filter(user=user).delete()
