from django.test import TestCase

from blog.forms import BlogPostForm
from shared.factories import ProfileFactory


class TestBlogPostform(TestCase):
    def setUp(self):
        super().setUp()
        self.profile = ProfileFactory.create()

    def test_form_blank(self):
        form = BlogPostForm(
            data={
                "title": "",
                "content": "",
            }
        )
        form_valid = form.is_valid()
        self.assertFalse(form_valid)
        self.assertEqual(len(form.errors["title"]), 1)
        self.assertEqual(len(form.errors["author"]), 1)
        self.assertEqual(len(form.errors["content"]), 1)

    def test_form_valid(self):
        form = BlogPostForm(
            data={
                "title": "First post",
                "content": "Hi there!",
                "author": self.profile.user,
            }
        )
        form_valid = form.is_valid()
        self.assertTrue(form_valid)
