from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, ContactMe, PostViewCount
from .forms import CommentForm, ContactForm, PostForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from users.views import get_user_location


def blog_home(request):
    template = 'blog/blog_home.html'
    all_posts = Post.objects.select_related("author").live_posts()
    new_posts = all_posts.new_posts()
    hot_posts = all_posts.hot_posts()
    featured_posts = all_posts.featured_posts()
    context = {
        'all_posts': all_posts,
        'new_posts': new_posts,
        'hot_posts': hot_posts,
        'featured_posts': featured_posts,
    }
    return render(request, template, context)


@login_required
def user_posts(request):
    live_posts = Post.objects.select_related("author").filter(author=request.user, is_live=True).order_by(
        '-date_posted')
    hidden_posts = Post.objects.select_related("author").filter(author=request.user, is_live=False).order_by(
        '-date_created')

    template = 'blog/blog_posts.html'
    context = {
        'live_posts':  live_posts,
        'live_posts_count': live_posts.count(),
        'hidden_posts': hidden_posts,
        'hidden_posts_count': hidden_posts.count()
    }

    return render(request, template, context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            # Create Post object but don't save to database yet
            obj = form.save(commit=False)
            # Save author as logged in user
            obj.author = request.user
            # If user sets 'is_live' status to True when creating new post, update 'date_posted' value to current time
            #  and notify user that post was published successfully. Otherwise notify that it was saved as draft.
            if obj.is_live:
                if obj.content:
                    obj.date_posted = timezone.now()
                    messages.success(request, f"""Your post "{obj.title}" was published successfully.""")
                # If user tries to create a new post with empty content, set 'is_live' to False and notify user
                else:
                    obj.is_live = False
                    messages.warning(request, f"""Your post "{obj.title}" was saved as draft as content is empty.""")
            else:
                messages.info(request, f"""Your post "{obj.title}" was successfully saved as draft.""")
            # Save post details to database
            obj.save()
            # Redirect to blog home
            return redirect('blog-home')

        else:
            messages.error(request, form.errors)

    else:
        form = PostForm()

    template = 'blog/blog_create.html'
    context = {'form': form}

    return render(request, template, context)


def record_view(request, obj=None, slug=None):
    """
    This function adds an entry in the PostViewCount table
    whenever a user accesses the particular web page.
    """
    if obj and obj.is_live:
        PostViewCount.objects.create(
            post=obj,
            ip=get_user_location(request)['ip'],
            country=get_user_location(request)['country'],
            city=get_user_location(request)['city'],
            timestamp=timezone.now()
        )


def post_detail(request, slug):
    # Get post
    post = get_object_or_404(Post.objects.select_related("author"), slug=slug)
    # Extract all approved comments for the specific post
    comments = Comment.objects.select_related("post", "owner").filter(post=post, status='APPROVED', is_live=True).order_by('date_created')
    # Extract all tags associated with the post

    # Capture IP Address of people visiting the page
    record_view(request, obj=post)

    # Comment form
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            obj = comment_form.save(commit=False)

            if post.is_live:
                # Reduce view count by one to avoid treating page redirect at time of submitting comment as 1 view
                post.views -= 1
                post.save()

                # Assign the current post to the comment
                obj.post = post
                # Assign post author to the comment
                obj.owner = post.author
                # Save the comment to the database
                if obj.content:
                    # Save comment to database
                    obj.save()
                    messages.success(
                        request,
                        # "Your comment has been sent to Moderator for review. It will be published if approved."
                        "Your comment was posted successfully."
                    )

            # Redirect back to the post-detail page
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()

    # Get count of comments
    post.comments = comments.count()
    # Get page views only of post is live. Increment views count by 1 for every page redirect or refresh
    if post.is_live:
        post.views += 1
    post.save()

    template_name = 'blog/blog_detail.html'
    context = {
        'post': post,
        'comments': comments,
        'comments_count': post.comments,
        'form': form
    }

    return render(request, template_name, context)


def edit_comment(request, pk):
    post = get_object_or_404(Post.objects.select_related("author"), pk=pk)
    comment = get_object_or_404(Comment.objects.select_related("owner", "post"), pk=pk)
    print(comment)
    # Get form data
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            # obj = form.save(commit=False)
            form.save()
    else:
        form = CommentForm(instance=comment)

    template = 'blog/commit_edit_modal.html'
    context = {
        'comment': comment,
        'form': form
    }

    return render(request, template, context)


@login_required
def post_update(request, slug):
    post = get_object_or_404(Post.objects.select_related("author"), author=request.user, slug=slug)

    # Comment posted
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            # Create Comment object but don't save to database yet
            obj = form.save(commit=False)
            # Save the post to the database only if user as added any content
            if obj.content:
                if obj.is_live:
                    if not obj.date_posted:
                        obj.date_posted = timezone.now()
                    messages.success(request, "Post updated successfully.")
                else:
                    messages.warning(request, "Your post was saved as draft successfully.")
            else:
                if obj.is_live:
                    obj.is_live = False
                    messages.warning(request, "Your post was saved as draft as content is empty.")
                else:
                    messages.warning(request, "Your post was saved as draft successfully.")

            if obj.is_live and obj.views > 0:
                obj.views -= 1

            obj.save()
            # Redirect user back to the post-detail page
            return redirect('blog-detail', slug=slug)

        # else:
        #     messages.error(request, form.errors)

    else:
        form = PostForm(instance=post)

    template_name = 'blog/blog_update.html'
    context = {
        # 'post': post,
        'form': form
    }

    return render(request, template_name, context)


def user_comments(request):
    approved = Comment.objects.select_related("post", "owner").approved_comments().order_by('-date_created')
    pending = Comment.objects.select_related("post", "owner").pending_comments().order_by('-date_created')
    reject = Comment.objects.select_related("post", "owner").rejected_comments().order_by('-date_created')

    template = 'blog/blog_comments.html'
    context = {
        'approved_comments':  approved,
        'approved_comments_count': approved.count(),
        'pending_comments':  pending,
        'pending_comments_count': pending.count(),
        'rejected_comments': reject,
        'rejected_comments_count': reject.count(),
    }

    return render(request, template, context)


def contact_admin(request):
    # Get content form data
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            from_email = form.cleaned_data['email']
            to = settings.EMAIL_HOST_USER
            subject = f"LordSipraSays | {form.cleaned_data['subject']} | " + \
                      f"{from_email}"
            body = render_to_string(
                'blog/contact_email.html', {
                    'user': form.cleaned_data['name'],
                    'message': form.cleaned_data['message'],
                }
            )

            # Send email to registered user
            send_email = EmailMessage(
                subject=subject,
                body=body,
                from_email=from_email,
                to=[to],
            )

            send_email.content_subtype = "html"
            send_email.send(fail_silently=False)
            messages.success(request, "Your email has been sent successfully.")
            return redirect('blog-home')

    else:
        form = ContactForm()

    template = 'blog/blog_contact_modal.html'
    context = {
        'form': form
    }

    return render(request, template, context)


def about_page(request):
    return render(request, 'blog/blog_about.html')
