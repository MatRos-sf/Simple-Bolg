from django.test import TestCase, Client

# Create your tests here.
from blog.models import Post


class SimpleTestObject(TestCase):
    def setUp(self):
        Post.objects.create(category='news', title='TEST',
                            body="TEST,TEST", tags="test")
        Post.objects.create(title='TEST2', body="ala", tags="test")
    def test_count_objects(self):
        count = Post.objects.count()
        self.assertEqual(count, 2)



