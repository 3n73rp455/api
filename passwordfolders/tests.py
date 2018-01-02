from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate, APITestCase, APIClient, APIRequestFactory
from core.models import User, Owner
from passwordfolders.models import PasswordFolder
from passwordfolders.views import PasswordFolderViewSet


class PasswordFolderTests(APITestCase):
    fixtures = ['owner.yaml', 'passwordtype.yaml', 'accesslevel.yaml']

    def setUp(self):
        User.objects.create_superuser(username='super', password='Welcome2', email='super@user.com')
        User.objects.create_user(username='regular', password='Welcome2', email='regular@user.com')
        superuser = User.objects.get(username='super')
        user = User.objects.get(username='regular')
        owner = Owner.objects.get(name='Personal')
        PasswordFolder.objects.create(name='Personal', description='Personal Folder', owner=owner, parent=None, user=superuser)
        PasswordFolder.objects.create(name='Personal', description='Personal Folder', owner=owner, parent=None, user=user)

    # List Password Folders as Test Superuser
    def test_passwordfolder_list_superuser(self):
        client = APIRequestFactory()
        user = User.objects.get(username='super')
        view = PasswordFolderViewSet.as_view({'get': 'list'})
        url = reverse('passwordfolder:passwordfolder-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # List Password Folders as Test User
    def test_passwordfolder_list_user(self):
        client = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordFolderViewSet.as_view({'get': 'list'})
        url = reverse('passwordfolder:passwordfolder-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieve Password Folder as Test Superuser
    def test_passwordfolder_retrieve_superuser(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='super')
        view = PasswordFolderViewSet.as_view({'get': 'retrieve'})
        url = reverse('passwordfolder:passwordfolder-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieve Password Folder as Test User
    def test_passwordfolder_retrieve_user(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordFolderViewSet.as_view({'get': 'retrieve'})
        url = reverse('passwordfolder:passwordfolder-detail', args=(User.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)