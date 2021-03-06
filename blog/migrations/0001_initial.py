# Generated by Django 3.0.3 on 2020-02-19 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ContactMe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Contact Me',
                'verbose_name_plural': 'Contact Me',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, default='', max_length=255, upload_to='blog')),
                ('views', models.PositiveIntegerField(default=0)),
                ('comments', models.PositiveIntegerField(default=0)),
                ('is_live', models.BooleanField(default=False, verbose_name='Publish Post')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_posted', models.DateTimeField(blank=True, default=None, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, default=None, to='blog.Category')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='TrendingPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255)),
                ('is_new', models.BooleanField(default=False, verbose_name='New Post')),
                ('is_hot', models.BooleanField(default=False, verbose_name='Hot Post')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured Post')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
            options={
                'verbose_name': 'Post - Trending',
                'verbose_name_plural': 'Post - Trending',
            },
        ),
        migrations.CreateModel(
            name='PostViewCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, default='', max_length=35)),
                ('ip', models.CharField(blank=True, default='', max_length=25)),
                ('country', models.CharField(blank=True, default='', max_length=50)),
                ('city', models.CharField(blank=True, default='', max_length=50)),
                ('timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
            options={
                'verbose_name': 'Post - View Count',
                'verbose_name_plural': 'Post - View Counts',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, help_text='Comments are moderated. Only those approved by the Moderator will be shown here.', null=True, verbose_name='Comment:')),
                ('status', models.CharField(choices=[('REJECT', 'REJECT'), ('PENDING', 'PENDING'), ('APPROVED', 'APPROVED')], default='APPROVED', max_length=10)),
                ('is_live', models.BooleanField(default=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(blank=True, default=None, null=True)),
                ('reviewed_by', models.CharField(blank=True, max_length=100)),
                ('review_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('review_notes', models.TextField(blank=True, default='', null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
            options={
                'verbose_name': 'Post - Comment',
                'verbose_name_plural': 'Post - Comments',
            },
        ),
    ]
