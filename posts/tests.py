from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='admin3',
            password="test12345"
            )

    def test_can_list_posts(self):
        admin3 = User.objects.get(username='admin3')
        Post.objects.create(owner=admin3, title='gemma title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(
            username='admin3',
            password='test12345'
            )
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PostDetailViewTests(APITestCase):
    def setUp(self):
        gemma = User.objects.create_user(
            username='gemma',
            password='pass'
        )
        tester = User.objects.create_user(
            username='tester',
            password='pass'
        )
        Post.objects.create(
            owner=gemma,
            title='gemmas title',
            content='gemmas content'
        )
        Post.objects.create(
            owner=tester,
            title='tester title',
            content='tester content'
        )
    def test_can_retreive_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'gemmas title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retreive_post_using_invalid_id(self):
        response = self.client.get('/posts/77')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_user_can_update_own_post(self):
        self.client.login(
            username='gemma',
            password='pass'
        )
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_cant_update_others_posts(self):
        """
        ***Issue with this test returning 200 response***
        """
        self.client.login(
            username='gemma',
            password='pass'
        )
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
