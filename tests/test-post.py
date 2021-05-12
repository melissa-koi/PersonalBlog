import unittest
from app.models import Post

class Post(unittest.TestCase):

    def setUp(self):
        self.post = Post(10,'title','content','author')

    def test_instance(self):
        self.assertTrue(isinstance(self.post,Post))