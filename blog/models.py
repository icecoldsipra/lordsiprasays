from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify
from .managers import PostManager, CommentManager


class Category(models.Model):
    tag = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.tag

    # def get_absolute_url(self):
    #    return reverse('blog-detail', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        slug = slugify(self.tag)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


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
    is_hot = models.BooleanField("Hot Post", default=False)
    is_featured = models.BooleanField("Featured Post", default=False)
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


class PostViewCount(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=35, default='', blank=True)
    ip = models.CharField(max_length=25, default='', blank=True)
    country = models.CharField(max_length=50, default='', blank=True)
    city = models.CharField(max_length=50, default='', blank=True)
    timestamp = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Post - View Count'
        verbose_name_plural = 'Post - View Counts'

    def __str__(self):
        return self.ip


class Comment(models.Model):
    COMMENT_CHOICES = (
        ("REJECT", "REJECT"),
        ("PENDING", "PENDING"),
        ("APPROVED", "APPROVED")
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField("Comment:", null=True, blank=True,
        help_text="Comments are moderated. Only those approved by the Moderator will be shown here.")
    status = models.CharField(max_length=10, choices=COMMENT_CHOICES, default="APPROVED")
    is_live = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, null=True, blank=True)
    reviewed_by = models.CharField(max_length=100, blank=True)
    review_time = models.DateTimeField(default=None, null=True, blank=True)
    review_notes = models.TextField(default='', blank=True, null=True)

    objects = CommentManager()

    class Meta:
        verbose_name = 'Post - Comment'
        verbose_name_plural = 'Post - Comments'

    def __str__(self):
        return self.owner

    def get_absolute_url(self):
        return reverse('edit-comment', kwargs={'pk': self.pk})


class ContactMe(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Contact Me'
        verbose_name_plural = 'Contact Me'

    def __str__(self):
        return self.subject
