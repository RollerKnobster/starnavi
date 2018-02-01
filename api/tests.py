from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Post, Like

# Create your tests here.


class UserModelTestCase(TestCase):
    """
    Testing user for creating instances.
    """

    def setUp(self):
        """
        Setting up the instances to save in tests.
        """
        self.username = "fuckboi"
        self.email = "djkhaled@mail.ru"
        self.password = "wethebest"
        self.user = User(username=self.username, email=self.email,
                         password=self.password)

    def test_model_can_create_a_user(self):
        """
        Test if the user model can create a user.
        """
        old_count = User.objects.count()
        self.user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)


class PostModelTestCase(TestCase):
    """
    Testing post for creating instances.
    """

    def setUp(self):
        """
        Setting up the instances to save in tests.
        """
        user = User.objects.create(username='djkhaled',
                                   email='djkhaled@gmail.com',
                                   password='wethebest')

        self.post_title = "Wild Thoughts hits #1 on billboard hot 100."
        self.post_body = "Seriously who gives a shit about dj khaled."
        self.post = Post(title=self.post_title, body=self.post_body,
                         author=user)

    def test_model_can_create_a_post(self):
        """
        Test if the post model can create a post.
        """
        old_count = Post.objects.count()
        self.post.save()
        new_count = Post.objects.count()
        self.assertNotEqual(old_count, new_count)


class LikeModelTestCase(TestCase):
    """
    Testing like for creating instances.
    """

    def setUp(self):
        """
        Setting up the instances to save in tests.
        """
        user = User.objects.create(username='djkhaled',
                                   email='djkhaled@gmail.com',
                                   password='wethebest')
        post = Post.objects.create(title='Wild Thoughts hits #1 on billboard',
                                   body='who gives a shit about dj khaled',
                                   author=user)

        self.like = Like(post=post, user=user)

    def test_model_can_create_a_like(self):
        """
        Test if the like model can create a like.
        """
        old_count = Like.objects.count()
        self.like.save()
        new_count = Like.objects.count()
        self.assertNotEqual(old_count, new_count)


class UserViewTestCase(TestCase):
    """
    Testing api view for user.
    """

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'djkhaled',
            'email': 'djkhaled@gmail.com',
            'password': 'wethebest'
        }
        self.response = self.client.post(reverse('user-list'), self.user_data)

    def test_api_can_create_a_user(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_get_is_enforced(self):
        response = self.client.get(reverse('user-detail', kwargs={
                                                            'pk': 1
                                                           }))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_get_a_user(self):
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('user-detail', kwargs={
                                                            'pk': user.pk
                                                           }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, user)

    def test_permissions_patch_delete_are_enforced(self):
        user = User.objects.get(id=1)
        new_user = User.objects.create(username='hey', email='hellome@mail.ru',
                                       password='heyheyhey')
        self.client.force_authenticate(user=user)
        user_data = {
            'username': 'newhey',
            'email': 'newhellome@mail.ru',
            'password': 'newheyheyhey'
        }
        response_patch = self.client.put(reverse('user-detail',
                                                   kwargs={'pk': new_user.pk}),
                                           user_data)
        response_delete = self.client.delete(reverse('user-detail',
                                                     kwargs={
                                                         'pk': new_user.pk
                                                     }))
        self.assertEqual(response_delete.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_patch.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_api_can_update_a_user(self):
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        user_data = {
            'username': 'newhey',
            'email': 'newhellome@mail.ru',
            'password': 'newheyheyhey'
        }
        response = self.client.patch(reverse('user-detail',
                                             kwargs={'pk': user.pk}),
                                     user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_a_user(self):
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        response = self.client.delete(reverse('user-detail',
                                              kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostViewTestCase(TestCase):
    """
    Testing api view for post.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='djkhaled1',
                                        email='djkhaled@mail.ru',
                                        password='wethebest')
        self.post_data = {
            'title': 'hell',
            'body': 'on earth'
        }
        self.response = self.client.post(reverse('post-list'), self.post_data)

    def test_authorization_create_is_enforced(self):
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_api_can_create_a_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('post-list'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authorization_get_is_enforced(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(reverse('post-list'), self.post_data)
        self.client.logout()
        post = Post.objects.get(author=self.user)
        response = self.client.get(reverse('post-detail', kwargs={
                                                            'pk': post.pk
                                                           }))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_get_a_post(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(reverse('post-list'), self.post_data)
        post = Post.objects.get(author=self.user)
        response = self.client.get(reverse('post-detail', kwargs={
                                                            'pk': post.pk
                                                          }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permissions_patch_delete_are_enforced(self):
        new_user = User.objects.create(username='hey', email='hellome@mail.ru',
                                       password='heyheyhey')
        new_post = Post.objects.create(title='fuck', body='shit',
                                       author=new_user)
        self.client.force_authenticate(user=self.user)
        post_data = {
            'title': 'newfuck',
            'body': 'newshit'
        }
        response_patch = self.client.put(reverse('post-detail',
                                                   kwargs={'pk': new_post.pk}),
                                           post_data)
        response_delete = self.client.delete(reverse('post-detail',
                                                     kwargs={
                                                         'pk': new_post.pk
                                                     }))

        self.assertEqual(response_delete.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_patch.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_api_can_update_a_post(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(reverse('post-list'), self.post_data)
        post = Post.objects.get(author=self.user)
        post_data = {
            'username': 'newhey',
            'email': 'newhellome@mail.ru',
            'password': 'newheyheyhey'
        }
        response = self.client.patch(reverse('post-detail',
                                             kwargs={'pk': post.pk}),
                                     post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_a_post(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(reverse('post-list'), self.post_data)
        post = Post.objects.get(author=self.user)
        response = self.client.delete(reverse('post-detail',
                                              kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
