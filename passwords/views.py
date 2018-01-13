from django.db.models import Q, FieldDoesNotExist
from django.http import Http404
from cryptography.fernet import InvalidToken
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from passwords.models import Password, PasswordACL, PasswordType
from passwords.permissions import (CanCreatePassword,
                                   CanListPassword,
                                   CanRetrievePassword,
                                   CanUpdatePassword,
                                   CanDestroyPassword,
                                   CanCreatePasswordACL,
                                   CanListPasswordACL,
                                   CanRetrievePasswordACL,
                                   CanUpdatePasswordACL,
                                   CanDestroyPasswordACL)
from passwords.serializers import PasswordSerializer, PasswordACLSerializer, PasswordTypeSerializer


# Password View
class PasswordViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Password.objects.all()
    serializer_class = PasswordSerializer
    permission_classes_by_action = {'list': [CanListPassword, IsAuthenticated],
                                    'create': [CanCreatePassword, IsAuthenticated],
                                    'retrieve': [CanRetrievePassword, IsAuthenticated],
                                    'update': [CanUpdatePassword, IsAuthenticated],
                                    'destroy': [CanDestroyPassword, IsAuthenticated]}

    def list(self, request, **kwargs):
        try:
            queryset = self.get_queryset().filter(Q(folder_id__passwordfolderacl__user=request.user) |
                                                  Q(folder__user=request.user, folder__personal=True))
            serializer = PasswordSerializer(queryset, many=True, context={'request': request})
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        try:
            serializer = PasswordSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            serializer = PasswordSerializer(instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (Http404, InvalidToken, TypeError):
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            serializer = PasswordSerializer(instance, data=request.data, context={'request': request})
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            self.perform_destroy(instance)
        except Password.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


# Password ACL View
# This view is only accessible by people with Owner or Admin privileges.
class PasswordACLViewSet(viewsets.ModelViewSet):
    queryset = PasswordACL.objects.all()
    serializer_class = PasswordACLSerializer
    permission_classes_by_action = {'list': [CanListPasswordACL],
                                    'create': [CanCreatePasswordACL],
                                    'retrieve': [CanRetrievePasswordACL],
                                    'update': [CanUpdatePasswordACL],
                                    'destroy': [CanDestroyPasswordACL]}

    def list(self, request, **kwargs):
        try:
            passwords = Password.objects.filter(passwordacl__in=self.get_queryset().filter(
                user=request.user)
            )
            queryset = self.get_queryset().filter(password__in=passwords)
        except TypeError:
            queryset = None
        serializer = PasswordACLSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        try:
            serializer = PasswordACLSerializer(data=request.data, context={'request': request})
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
            serializer = PasswordACLSerializer(instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Password.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            serializer = PasswordACLSerializer(instance, context={'request': request})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def destroy(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            self.perform_destroy(instance)
        except PasswordACL.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class PasswordTypeViewSet(viewsets.ModelViewSet):
    queryset = PasswordType.objects.all()
    serializer_class = PasswordTypeSerializer
