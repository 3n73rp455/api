from django.contrib.auth.hashers import make_password
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response

from core.models import User, AccessLevel, Owner, SystemSetting
from core.permissions import (CanListUser,
                              CanRetrieveUser,
                              CanCreateUser,
                              CanUpdateUser,
                              CanDestroyUser,
                              CanListAccessLevel,
                              CanRetrieveAccessLevel,
                              CanCreateAccessLevel,
                              CanUpdateAccessLevel,
                              CanDestroyAccessLevel,
                              CanListOwner,
                              CanRetrieveOwner,
                              CanCreateOwner,
                              CanUpdateOwner,
                              CanDestroyOwner,
                              )
from core.serializers import UserSerializer, AccessLevelSerializer, OwnerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {'list': [CanListUser],
                                    'create': [CanCreateUser],
                                    'retrieve': [CanRetrieveUser],
                                    'update': [CanUpdateUser],
                                    'destroy': [CanDestroyUser]}

    def list(self, request, **kwargs):
        try:
            queryset = self.get_queryset()
        except TypeError:
            queryset = None
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        try:
            password = make_password(request.data['password'])
            serializer = UserSerializer(data=request.data, context={'request': request})
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save(password=password)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            serializer = UserSerializer(instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None, **kwargs):
        try:
            password = make_password(request.data['password'])
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            serializer = UserSerializer(instance, data=request.data, context={'request': request})
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save(password=password)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            self.perform_destroy(instance)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class AccessLevelViewSet(viewsets.ModelViewSet):
    queryset = AccessLevel.objects.all()
    serializer_class = AccessLevelSerializer
    permission_classes_by_action = {'list': [CanListAccessLevel],
                                    'create': [CanCreateAccessLevel],
                                    'retrieve': [CanRetrieveAccessLevel],
                                    'update': [CanUpdateAccessLevel],
                                    'destroy': [CanDestroyAccessLevel]}

    def list(self, request, **kwargs):
        try:
            queryset = self.get_queryset()
        except TypeError:
            queryset = None
        serializer = AccessLevelSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            serializer = AccessLevelSerializer(instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes_by_action = {'list': [CanListOwner],
                                    'create': [CanCreateOwner],
                                    'retrieve': [CanRetrieveOwner],
                                    'update': [CanUpdateOwner],
                                    'destroy': [CanDestroyOwner]}

    def list(self, request, **kwargs):
        try:
            queryset = self.get_queryset()
        except TypeError:
            queryset = None
        serializer = OwnerSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(self.request, instance)
            serializer = OwnerSerializer(instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
