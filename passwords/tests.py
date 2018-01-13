from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate, APITestCase, APIClient, APIRequestFactory
from core.models import User, Owner, AccessLevel
from passwordfolders.models import PasswordFolder, PasswordFolderACL
from passwords.models import Password, PasswordACL, PasswordType
from passwords.views import PasswordViewSet


class PasswordAPITestCase(APITestCase):
    fixtures = ['owner.yaml', 'passwordtype.yaml', 'accesslevel.yaml']

    def setUp(self):
        User.objects.create_user(username='regular', password='Welcome2', email='regular@user.com')
        user = User.objects.get(username='regular')
        shared = Owner.objects.get(name='Default')
        password_type = PasswordType.objects.get(name='Web')
        PasswordFolder.objects.create(name='Shared',
                                      description='Shared Folder',
                                      owner=shared,
                                      parent=None,
                                      user=user)
        personal_folder = PasswordFolder.objects.get(name='Personal', user=user)
        shared_folder = PasswordFolder.objects.get(name='Shared')
        owner_level = AccessLevel.objects.get(name='Owner')
        Password.objects.create(name='Test Personal',
                                description='Test Personal Password',
                                type=password_type,
                                username='test_user',
                                password='123456',
                                url='http://test.com',
                                folder=personal_folder)
        Password.objects.create(name='Test Shared',
                                description='Test Shared Password',
                                type=password_type,
                                username='test_user',
                                password='12345678',
                                url='http://test.com',
                                folder=shared_folder)
        PasswordFolderACL.objects.create(user=user,
                                         folder=shared_folder,
                                         level=owner_level)

    # List Password Folders as Test User
    def test_password_list(self):
        client = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordViewSet.as_view({'get': 'list'})
        url = reverse('password:password-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Password.objects.count(), 2)

    # Retrieve Personal Password as Test User
    def test_password_personal_detail(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordViewSet.as_view({'get': 'retrieve'})
        url = reverse('password:password-detail', args=(Password.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieve Shared Password as Test User
    def test_password_shared_detail(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordViewSet.as_view({'get': 'retrieve'})
        url = reverse('password:password-detail', args=(Password.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordViewSet.as_view({'post': 'create'})
        url = reverse('password:password-list')
        data = {
            'name': 'Test Password',
            'description': 'Test Password Addition',
            'type': '1',
            'username': 'test_create',
            'password': '123456',
            'url': 'http://create.com',
            'folder': '2',
            'tags': []
        }
        request = factory.post(url, data)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Password.objects.count(), 3)

    # Put Password as Test User
    def test_password_put(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordViewSet.as_view({'post': 'update'})
        url = reverse('password:password-detail', args=(Password.pk,))
        data = {
            'name': 'Test Password',
            'description': 'Test Password Addition',
            'type': '1',
            'username': 'test_create',
            'password': '123456',
            'url': 'http://create.com',
            'folder': '2',
            'tags': []
        }
        request = factory.post(url, data)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    # Destroy Password as Test User
    def test_password_destroy(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordViewSet.as_view({'post': 'destroy'})
        url = reverse('password:password-detail', args=(Password.pk,))
        request = factory.post(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PasswordACLAPITestCase(APITestCase):
    fixtures = ['owner.yaml', 'passwordtype.yaml', 'accesslevel.yaml']

    def setUp(self):
        User.objects.create_user(username='regular', password='Welcome2', email='regular@user.com')
        user = User.objects.get(username='regular')
        shared = Owner.objects.get(name='Default')
        password_type = PasswordType.objects.get(name='Web')
        PasswordFolder.objects.create(name='Shared',
                                      description='Shared Folder',
                                      owner=shared,
                                      parent=None,
                                      user=user)
        personal_folder = PasswordFolder.objects.get(name='Personal', user=user)
        shared_folder = PasswordFolder.objects.get(name='Shared')
        owner_level = AccessLevel.objects.get(name='Owner')
        Password.objects.create(name='Test Personal',
                                description='Test Personal Password',
                                type=password_type,
                                username='test_user',
                                password='123456',
                                url='http://test.com',
                                folder=personal_folder)
        Password.objects.create(name='Test Shared',
                                description='Test Shared Password',
                                type=password_type,
                                username='test_user',
                                password='123456',
                                url='http://test.com',
                                folder=shared_folder)
        PasswordFolderACL.objects.create(user=user,
                                         folder=shared_folder,
                                         level=owner_level)

    # List Password Folders as Test User
    def test_passwordacl_list(self):
        client = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordViewSet.as_view({'get': 'list'})
        url = reverse('password:passwordacl-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PasswordACL.objects.count(), 0)
