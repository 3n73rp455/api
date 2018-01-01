from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate, APITestCase, APIClient, APIRequestFactory
from core.models import User
from core.views import UserViewSet


class UserTests(APITestCase):
    fixtures = ['owner.yaml', 'passwordtype.yaml', 'accesslevel.yaml']

    # Register Test User
    def test_register_user(self):
        client = APIClient()
        url = reverse('rest_register')
        payload = {
            'username': 'test',
            'password1': 'Welcome2',
            'password2': 'Welcome2',
            'email': 'test@user.com'
        }
        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')

    # Register Test User
    def test_login_user(self):
        User.objects.create_user(username='test', password='Welcome2', email='test@user.com')
        client = APIClient()
        url = reverse('rest_login')
        payload = {
            'username': 'test',
            'password': 'Welcome2'
        }
        response = client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list(self):
        client = APIRequestFactory()
        User.objects.create_superuser(username='test', password='Welcome2', email='test@user.com')
        user = User.objects.get(username='test')
        view = UserViewSet.as_view({'get': 'list'})
        url = reverse('core:user-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        factory = APIRequestFactory()
        User.objects.create_superuser(username='test', password='Welcome2', email='test@user.com')
        user = User.objects.get(username='test')
        view = UserViewSet.as_view({'get': 'retrieve'})
        url = reverse('core:user-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)