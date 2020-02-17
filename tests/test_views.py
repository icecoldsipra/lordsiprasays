from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post, PostViewCount, Comment, Contact, Category


class TestBlogViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.blog_home_url = reverse('blog-home')
        self.user_posts_url = reverse('blog-posts')

    def test_blog_home_GET_PASS(self):
        response = self.client.get(self.blog_home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_home.html')
        print("blog-home GET_PASS view test completed")

    def test_blog_home_GET_FAIL_wrong_status_code(self):
        response = self.client.get(self.blog_home_url)
        self.assertNotEquals(response.status_code, 404)
        print("blog-home GET_FAIL_1 view test completed")

    def test_blog_home_GET_FAIL_2_wrong_template(self):
        response = self.client.get(self.blog_home_url)
        self.assertTemplateNotUsed(response, 'blog/blog_profile.html')
        print("blog-home GET_FAIL_2 view test completed")

    def test_blog_home_GET_FAIL_3_empty_data(self):
        pass

    def test_user_posts(self):
        response = self.client.get(self.user_posts_url)