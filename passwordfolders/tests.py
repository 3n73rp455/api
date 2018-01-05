from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate, APITestCase, APIClient, APIRequestFactory
from core.models import User, Owner
from passwordfolders.models import PasswordFolder, PasswordFolderACL
from passwordfolders.views import PasswordFolderViewSet


class PasswordFolderAPITestCase(APITestCase):
    fixtures = ['owner.yaml', 'passwordtype.yaml', 'accesslevel.yaml']

    def setUp(self):
        User.objects.create_superuser(username='super', password='Welcome2', email='super@user.com')
        User.objects.create_user(username='regular', password='Welcome2', email='regular@user.com')
        superuser = User.objects.get(username='super')
        user = User.objects.get(username='regular')
        personal = Owner.objects.get(name='Personal')
        shared = Owner.objects.get(name='Default')
        PasswordFolder.objects.create(name='Shared', description='Shared Folder', owner=shared, parent=None, user=user)

    # List Password Folders as Test User
    def test_passwordfolder_list(self):
        client = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordFolderViewSet.as_view({'get': 'list'})
        url = reverse('passwordfolder:passwordfolder-list')
        request = client.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieve Password Folder as Test User
    def test_passwordfolder_detail(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordFolderViewSet.as_view({'get': 'retrieve'})
        url = reverse('passwordfolder:passwordfolder-detail', args=(PasswordFolder.pk,))
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, pk=2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Create Password Folder as Test User
    def test_passwordfolder_private_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordFolderViewSet.as_view({'post': 'create'})
        url = reverse('passwordfolder:passwordfolder-list')
        data = {
            'name': 'Test Folder',
            'description': 'Test User Folder Addition',
            'owner': '2',
            'personal': 'True',
            'parent': '',
            'tags': []
        }
        request = factory.post(url, data)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_passwordfolder_shared_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordFolderViewSet.as_view({'post': 'create'})
        url = reverse('passwordfolder:passwordfolder-list')
        data = {
            'name': 'Test Folder',
            'description': 'Test User Folder Addition',
            'owner': '1',
            'personal': 'False',
            'parent': '',
            'tags': []
        }
        request = factory.post(url, data)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PasswordFolderACL.objects.count(), 3)


    # Patch Password Folder as Test User
    def test_passwordfolder_private_patch(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordFolderViewSet.as_view({'post': 'partial_update'})
        url = reverse('passwordfolder:passwordfolder-detail', args=(PasswordFolder.pk,))
        data = {
            'name': 'Test Folder',
            'description': 'Test User Folder Patch',
            'owner': '2',
            'personal': 'True',
            'parent': '',
            'tags': []
        }
        request = factory.post(url, data)
        force_authenticate(request, user=user)
        response = view(request, pk=2)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    # Destroy Password Folder as Test User
    def test_passwordfolder_private_destroy(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='regular')
        view = PasswordFolderViewSet.as_view({'post': 'destroy'})
        url = reverse('passwordfolder:passwordfolder-detail', args=(PasswordFolder.pk,))
        request = factory.post(url)
        force_authenticate(request, user=user)
        response = view(request, pk=2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)