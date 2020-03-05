from django.db import models


class PostQuerySet(models.QuerySet):
    def live_posts(self):
        return self.filter(is_live=True).order_by('-date_posted')

    def hidden_posts(self):
        return self.filter(is_live=False)

    def user_posts(self, user):
        return self.filter(author=user)

    def new_posts(self):
        return self.filter(is_live=True).order_by('-date_posted')

    def hot_posts(self):
        return self.filter(is_hot=True).order_by('-date_posted')

    def featured_posts(self):
        return self.filter(is_featured=True).order_by('-date_posted')


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def live_posts(self):
        return self.get_queryset().live_posts()

    def hidden_posts(self):
        return self.get_queryset().hidden_posts()

    def user_posts(self, user):
        return self.get_queryset().user_posts(user)

    def new_posts(self):
        return self.get_queryset().new_posts()

    def hot_posts(self):
        return self.get_queryset().hot_posts()

    def featured_posts(self):
        return self.get_queryset().featured_posts()


class CommentQuerySet(models.QuerySet):
    def approved_comments(self):
        return self.filter(status="APPROVED")

    def pending_comments(self):
        return self.filter(status="PENDING")

    def rejected_comments(self):
        return self.filter(status="REJECT")

    def live_comments(self):
        return self.filter(is_live=True)

    def edited_comments(self):
        return self.filter(is_edited=True)


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def approved_comments(self):
        return self.get_queryset().approved_comments()

    def pending_comments(self):
        return self.get_queryset().pending_comments()

    def rejected_comments(self):
        return self.get_queryset().rejected_comments()

    def live_comments(self):
        return self.get_queryset().live_comments()

    def edited_comments(self):
        return self.get_queryset().edited_comments()
