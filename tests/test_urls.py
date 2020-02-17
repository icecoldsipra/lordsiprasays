from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import (
    UserLoginView, UserLogoutView, UserRegisterView, users_activate, UserUpdateView, UserPasswordResetView,
    UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView, validate_email,
    validate_username, UserPasswordChangeView, UserPasswordChangeDoneView
)
from blog.views import (
    blog_home, user_posts, post_create, post_detail, post_update, user_comments, about_page, contact_admin,
    edit_comment
)


class TestUsersUrls(SimpleTestCase):
    def test_users_login(self):
        url = reverse('users-login')
        self.assertEquals(resolve(url).func.view_class, UserLoginView)
        print("users-login test completed.")

    def test_users_logout(self):
        url = reverse('users-logout')
        self.assertEquals(resolve(url).func.view_class, UserLogoutView)
        print("users-logout test completed.")

    def test_users_register(self):
        url = reverse('users-register')
        self.assertEquals(resolve(url).func.view_class, UserRegisterView)
        print("users-register test completed.")

    def test_users_activate(self):
        url = reverse('users-activate', args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func, users_activate)
        print("users-activate test completed.")

    def test_validate_email(self):
        url = reverse('validate-email')
        self.assertEquals(resolve(url).func, validate_email)
        print("validate-email test completed.")

    def test_validate_username(self):
        url = reverse('validate-username')
        self.assertEquals(resolve(url).func, validate_username)
        print("validate-username test completed.")

    def test_password_change(self):
        url = reverse('password-change')
        self.assertEquals(resolve(url).func.view_class, UserPasswordChangeView)
        print("password-change test completed.")

    def test_password_change_done(self):
        url = reverse('password-change-done')
        self.assertEquals(resolve(url).func.view_class, UserPasswordChangeDoneView)
        print("password-change-done test completed.")

    def test_password_reset(self):
        url = reverse('password-reset')
        self.assertEquals(resolve(url).func.view_class, UserPasswordResetView)
        print("password-reset test completed.")

    def test_password_reset_done(self):
        url = reverse('password-reset-done')
        self.assertEquals(resolve(url).func.view_class, UserPasswordResetDoneView)
        print("password-reset-done test completed.")

    def test_password_reset_confirm(self):
        url = reverse('password-reset-confirm', args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func.view_class, UserPasswordResetConfirmView)
        print("password-reset-confirm test completed.")

    def test_password_reset_complete(self):
        url = reverse('password-reset-complete')
        self.assertEquals(resolve(url).func.view_class, UserPasswordResetCompleteView)
        print("password-reset-complete test completed.")

    def test_users_profile(self):
        url = reverse('users-profile', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, UserUpdateView)
        print("users-profile test completed.")


class TestBlogUrls(SimpleTestCase):
    def test_blog_home(self):
        url = reverse('blog-home')
        self.assertEquals(resolve(url).func, blog_home)
        print("blog-home test completed.")

    def test_user_posts(self):
        url = reverse('blog-posts')
        self.assertEquals(resolve(url).func, user_posts)
        print("blog-posts test completed.")

    def test_post_create(self):
        url = reverse('blog-create')
        self.assertEquals(resolve(url).func, post_create)
        print("blog-create test completed.")

    def test_post_detail(self):
        url = reverse('blog-detail', args=['slug'])
        self.assertEquals(resolve(url).func, post_detail)
        print("blog-detail test completed.")

    def test_post_update(self):
        url = reverse('blog-update', args=['slug'])
        self.assertEquals(resolve(url).func, post_update)
        print("blog-update test completed.")

    def test_user_comments(self):
        url = reverse('blog-comments')
        self.assertEquals(resolve(url).func, user_comments)
        print("blog-comments test completed.")

    def test_about_page(self):
        url = reverse('blog-about')
        self.assertEquals(resolve(url).func, about_page)
        print("blog-about test completed.")

    def test_contact_admin(self):
        url = reverse('blog-contact')
        self.assertEquals(resolve(url).func, contact_admin)
        print("blog-contact test completed.")

    """
    def test_edit_comment(self):
        url = reverse('edit-comment')
        self.assertEquals(resolve(url).func, edit_comment)
        print("edit-comment test completed.")
    """