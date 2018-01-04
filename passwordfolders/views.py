import json
from django.http import Http404
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response

from core.models import AccessLevel
from passwordfolders.models import PasswordFolder, PasswordFolderACL
from passwordfolders.permissions import (CanCreatePasswordFolder,
                                         CanListPasswordFolder,
                                         CanRetrievePasswordFolder,
                                         CanUpdatePasswordFolder,
                                         CanDestroyPasswordFolder,
                                         CanCreatePasswordFolderACL,
                                         CanListPasswordFolderACL,
                                         CanRetrievePasswordFolderACL,
                                         CanDestroyPasswordFolderACL,
                                         )
from passwordfolders.serializers import PasswordFolderSerializer, PasswordFolderACLSerializer


# Password Folder ACL View
# This view is only accessible by people with Owner or Admin privileges for their respective Password Folders.
class PasswordFolderACLViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = PasswordFolderACL.objects.all()
    serializer_class = PasswordFolderACLSerializer
    permission_classes_by_action = {'create': [CanCreatePasswordFolderACL],
                                    'list': [CanListPasswordFolderACL],
                                    'retrieve': [CanRetrievePasswordFolderACL],
                                    'destroy': [CanDestroyPasswordFolderACL]}

    def list(self, request, **kwargs):
        try:
            folders = PasswordFolder.objects.filter(passwordfolderacl__in=self.get_queryset().filter(
                user=request.user, level__name__in=['Owner', 'Admin'])
            )
            queryset = self.get_queryset().filter(folder__in=folders)
        except TypeError:
            queryset = None
        serializer = PasswordFolderACLSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        try:
            serializer = PasswordFolderACLSerializer(data=request.data, context={'request': request})
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            serializer = PasswordFolderACLSerializer(instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            self.perform_destroy(instance)
        except PasswordFolderACL.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


# Password Folder View
class PasswordFolderViewSet(viewsets.ModelViewSet):
    queryset = PasswordFolder.objects.all()
    serializer_class = PasswordFolderSerializer
    permission_classes_by_action = {'create': [CanCreatePasswordFolder],
                                    'list': [CanListPasswordFolder],
                                    'retrieve': [CanRetrievePasswordFolder],
                                    'partial_update': [CanUpdatePasswordFolder],
                                    'update': [CanUpdatePasswordFolder],
                                    'destroy': [CanDestroyPasswordFolder]}

    def list(self, request, **kwargs):
        access_levels = AccessLevel.objects.filter(name__in=['Owner', 'Admin', 'Modify', 'Read'])
        try:
            queryset = self.get_queryset().filter(Q(
                passwordfolderacl__user=request.user,
                passwordfolderacl__level__in=access_levels) | Q(personal=True, user=request.user)
            )
            serializer = PasswordFolderSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        except TypeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, **kwargs):
        serializer = PasswordFolderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            serializer = PasswordFolderSerializer(instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            serializer = PasswordFolderSerializer(instance, data=request.data, context={'request': request})
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            acl_instances = PasswordFolderACL.objects.filter(folder=pk)
            self.check_object_permissions(self.request, instance)
            # destroy all associated ACL objects
            for i in acl_instances:
                self.perform_destroy(i)
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
