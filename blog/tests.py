from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Task

# Patch Django test instrumentation bug in Python 3.14
import django.test.client
django.test.client.store_rendered_templates = lambda *args, **kwargs: None

class BlogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='password123', email='test@test.com')

    def test_redirect_if_not_logged_in(self):
        # Home should redirect
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_login_and_home(self):
        self.client.login(username='tester', password='password123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Django Lab')
        self.assertContains(response, 'tester')

    def test_create_post(self):
        self.client.login(username='tester', password='password123')
        response = self.client.post(reverse('post_create'), {
            'title': 'Test Post',
            'content': 'This is a test post.',
            'is_published': True
        })
        # Should redirect to post_detail
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)

    def test_create_task(self):
        self.client.login(username='tester', password='password123')
        response = self.client.post(reverse('task_form'), {
            'title': 'Explore Django test',
            'description': 'Description',
            'status': 'pending',
            'due_date': '2030-01-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Explore Django test')
        # Check session message
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Task "Explore Django test" created!' in str(m) for m in messages))
