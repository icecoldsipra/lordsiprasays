from django.test import TestCase
from users.models import CustomUser


class TestUsersModel(TestCase):
    def test_slug_generator(self):
        self.test1 = CustomUser.objects.create(
            username='test1',
            email='test1@test.com',
            first_name='test',
            last_name='test',
        )
        self.test2 = CustomUser.objects.create(
            username='test2',
            email='test2@test.com',
            first_name='test',
            last_name='test',
        )
        self.test3 = CustomUser.objects.create(
            username='test3',
            email='test3@test.com',
            first_name='test',
        )
        self.test4 = CustomUser.objects.create(
            username='test4',
            email='test4@test.com',
            first_name='test',
        )

        self.assertEquals(self.test1.slug, 'test-test')
        self.assertEquals(self.test2.slug, 'test-test-1')
        self.assertEquals(self.test3.slug, 'test')
        self.assertEquals(self.test4.slug, 'test-1')
        self.assertNotEquals(self.test3.slug, 'test-1')
        print("CustomUser slug test completed.")

