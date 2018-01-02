from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate, APITestCase, APIClient, APIRequestFactory
from core.models import User
from core.views import UserViewSet


class AuthTests(APITestCase):
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

    # Login Test User
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


class UserTests(APITestCase):
    fixtures = ['owner.yaml', 'passwordtype.yaml', 'accesslevel.yaml']

    def setUp(self):
        User.objects.create_superuser(username='super', password='Welcome2', email='super@user.com')
        User.objects.create_user(username='regular', password='Welcome2', email='regular@user.com')

    # List Users as Test Superuser
    def test_user_list_superuser(self):
        client = APIRequestFactory()
        user = User.objects.get(username='super')
        view = UserViewSet.as_view({'get': 'list'})
        url = reverse('core:user-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # List Users as Test User
    def test_user_list_user(self):
        client = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = UserViewSet.as_view({'get': 'list'})
        url = reverse('core:user-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Retrieve User as Test Superuser
    def test_user_retrieve_superuser(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='super')
        view = UserViewSet.as_view({'get': 'retrieve'})
        url = reverse('core:user-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieve User as Test User
    def test_user_retrieve_user(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = UserViewSet.as_view({'get': 'retrieve'})
        url = reverse('core:user-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AccessLevelTests(APITestCase):
    fixtures = ['owner.yaml', 'passwordtype.yaml', 'accesslevel.yaml']

    def setUp(self):
        User.objects.create_superuser(username='super', password='Welcome2', email='super@user.com')
        User.objects.create_user(username='regular', password='Welcome2', email='regular@user.com')

    # List Access Levels as Test Superuser
    def test_accesslevel_list_superuser(self):
        client = APIRequestFactory()
        user = User.objects.get(username='super')
        view = UserViewSet.as_view({'get': 'list'})
        url = reverse('core:accesslevel-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # List Access Levels as Test User
    def test_accesslevel_list_user(self):
        client = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = UserViewSet.as_view({'get': 'list'})
        url = reverse('core:accesslevel-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Retrieve Access Levels as Test Superuser
    def test_accesslevel_retrieve_superuser(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='super')
        view = UserViewSet.as_view({'get': 'retrieve'})
        url = reverse('core:accesslevel-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieve Access Levels as Test User
    def test_accesslevel_retrieve_user(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = UserViewSet.as_view({'get': 'retrieve'})
        url = reverse('core:accesslevel-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OwnerTests(APITestCase):
    fixtures = ['owner.yaml', 'passwordtype.yaml', 'accesslevel.yaml']

    def setUp(self):
        User.objects.create_superuser(username='super', password='Welcome2', email='super@user.com')
        User.objects.create_user(username='regular', password='Welcome2', email='regular@user.com')

    # List Owners as Test Superuser
    def test_owner_list_superuser(self):
        client = APIRequestFactory()
        user = User.objects.get(username='super')
        view = UserViewSet.as_view({'get': 'list'})
        url = reverse('core:owner-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # List Owners as Test User
    def test_owner_list_user(self):
        client = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = UserViewSet.as_view({'get': 'list'})
        url = reverse('core:owner-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Retrieve Owners as Test Superuser
    def test_owner_retrieve_superuser(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='super')
        view = UserViewSet.as_view({'get': 'retrieve'})
        url = reverse('core:owner-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieve Owners as Test User
    def test_owner_retrieve_user(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = UserViewSet.as_view({'get': 'retrieve'})
        url = reverse('core:owner-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SystemSettingTests(APITestCase):
    fixtures = ['owner.yaml', 'passwordtype.yaml', 'accesslevel.yaml']

    def setUp(self):
        User.objects.create_superuser(username='super', password='Welcome2', email='super@user.com')
        User.objects.create_user(username='regular', password='Welcome2', email='regular@user.com')

    # List System Settings as Test Superuser
    def test_systemsetting_list_superuser(self):
        client = APIRequestFactory()
        user = User.objects.get(username='super')
        view = UserViewSet.as_view({'get': 'list'})
        url = reverse('core:systemsetting-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # List System Settings as Test User
    def test_systemsetting_list_user(self):
        client = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = UserViewSet.as_view({'get': 'list'})
        url = reverse('core:systemsetting-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Retrieve System Settings as Test Superuser
    def test_systemsetting_retrieve_superuser(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='super')
        view = UserViewSet.as_view({'get': 'retrieve'})
        url = reverse('core:systemsetting-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieve System Settings as Test User
    def test_systemsetting_retrieve_user(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = UserViewSet.as_view({'get': 'retrieve'})
        url = reverse('core:systemsetting-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
