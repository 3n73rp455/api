from django.db.models import Q
from rest_framework import permissions
from core.models import AccessLevel
from core.permissions import is_application, is_servicedesk, is_superuser, is_support
from passwords.models import Password, PasswordACL
from passwordfolders.models import PasswordFolderACL, PasswordFolder


# Password Permission per Object based on folder ACL
def get_permission_level(request, obj):
    if request.user == 'AnonymousUser':
        level = None
        return level
    else:
        try:
            level = PasswordFolderACL.objects.get(folder=obj.folder, user=request.user)
        except AttributeError:
            acl = PasswordACL.objects.get(pk=obj.id)
            password = Password.objects.get(pk=acl.password.pk)
            level = PasswordFolderACL.objects.get(folder=password.folder, user=request.user)
        except:
            level = None
        return level


# Password Permissions
class CanListPassword(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user:
            if request.user == 'AnonymousUser':
                return False
            return True


class CanCreatePassword(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            for r in request.data:
                folder_id = request.data['folder']
                if folder_id == '':
                    return True
                else:
                    folder_level = PasswordFolderACL.objects.get(folder__id=folder_id, user=request.user)
                    if folder_level.level.name in ['Owner', 'Admin']:
                        return True
                    else:
                        return False
            return True


class CanRetrievePassword(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        access_levels = ['Owner', 'Admin', 'Modify', 'Read']
        if get_permission_level(request, obj) is None:
            return False
        else:
            level = AccessLevel.objects.get(pk=get_permission_level(request, obj).level_id).name
            if level in access_levels:
                return True
            else:
                return False


class CanUpdatePassword(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        access_levels = ['Owner', 'Admin', 'Modify']
        if get_permission_level(request, obj) is None:
            return False
        else:
            level = AccessLevel.objects.get(pk=get_permission_level(request, obj).level_id).name
            if level in access_levels:
                return True
            else:
                return False


class CanDestroyPassword(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        access_levels = ['Owner', 'Admin']
        if get_permission_level(request, obj) is None:
            return False
        else:
            level = AccessLevel.objects.get(pk=get_permission_level(request, obj).level_id).name
            if level in access_levels:
                return True
            else:
                return False


# Password ACL Permissions
class CanListPasswordACL(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True


class CanCreatePasswordACL(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            password = request.data['password']
            folder = PasswordFolder.objects.get(pk=password)
            folder_level = PasswordFolderACL.objects.get(folder=folder, user=request.user)
            if folder_level.level.name in ['Owner', 'Admin']:
                return True
            else:
                return False


class CanRetrievePasswordACL(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        access_levels = ['Owner', 'Admin', 'Modify', 'Read']
        if get_permission_level(request, obj) is None:
            return False
        else:
            level = AccessLevel.objects.get(pk=get_permission_level(request, obj).level_id).name
            print('test')
            if level in access_levels:
                return True
            else:
                return False


class CanUpdatePasswordACL(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        access_levels = ['Owner', 'Admin', 'Modify']
        if get_permission_level(request, obj) is None:
            return False
        else:
            level = AccessLevel.objects.get(pk=get_permission_level(request, obj).level_id).name
            if level in access_levels:
                return True
            else:
                return False


class CanDestroyPasswordACL(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        access_levels = ['Owner', 'Admin']
        if get_permission_level(request, obj) is None:
            return False
        else:
            level = AccessLevel.objects.get(pk=get_permission_level(request, obj).level_id).name
            print(level)
            if level in access_levels:
                return True
            else:
                return False
