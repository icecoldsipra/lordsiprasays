from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify
from .managers import PostManager, CommentManager


class Category(models.Model):
    tag = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    tags = models.ManyToManyField(Category, default=None, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(max_length=255, upload_to='blog', default='', blank=True)
    views = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    is_live = models.BooleanField("Publish Post", default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_posted = models.DateTimeField(default=None, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = PostManager()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


COMMENT_CHOICES = (
    ("REJECT", "REJECT"),
    ("PENDING", "PENDING"),
    ("APPROVED", "APPROVED")
)


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField("Comments:", null=True, blank=True,
        help_text="Comments are moderated. Only those approved by the Moderator will be shown here.")
    status = models.CharField(max_length=10, choices=COMMENT_CHOICES, default="PENDING")
    timestamp = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.CharField(max_length=100, blank=True)
    review_time = models.DateTimeField(default=None, null=True, blank=True)
    review_notes = models.TextField(default='', blank=True, null=True)

    objects = CommentManager()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"{self.name} : {self.post}"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.subject
