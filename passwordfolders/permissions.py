from rest_framework import permissions
from core.models import AccessLevel
from passwordfolders.models import PasswordFolderACL, PasswordFolder


# Password Folder Permissions
def get_permission_level(request, obj):
    if request.user == 'AnonymousUser':
        level = None
        return level
    else:
        try:
            level = PasswordFolderACL.objects.get(folder=obj, user=request.user)
        except:
            level = None
        return level


# Password Folder Permissions
class CanListPasswordFolder(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True


class CanCreatePasswordFolder(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            for r in request.data:
                parent_name = request.data['parent']
                if parent_name == '':
                    return True
                else:
                    parent_level = PasswordFolderACL.objects.get(folder__name=parent_name, user=request.user)
                    if parent_level.level.name in ['Owner', 'Admin']:
                        return True
                    else:
                        return False
            return True


class CanRetrievePasswordFolder(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        access_levels = ['Owner', 'Admin', 'Read']
        if get_permission_level(request, obj) is None:
            if obj.personal:
                if request.user == obj.user:
                    return True
                else:
                    return False
            else:
                return False
        else:
            level = AccessLevel.objects.get(pk=get_permission_level(request, obj).level_id).name
            if level in access_levels:
                return True
            else:
                return False


class CanUpdatePasswordFolder(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        level = get_permission_level(request, obj).level.name
        if level in ['Owner', 'Admin']:
            return True
        else:
            return False


class CanDestroyPasswordFolder(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        try:
            level = get_permission_level(request, obj).level.name
        except AttributeError:
            return False
        if level in ['Owner']:
            return True
        else:
            return False


# Password Folder ACL Permissions
class CanCreatePasswordFolderACL(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            for r in request.data:
                folder_name = request.data['folder']
                folder_type = PasswordFolder.objects.get(name=folder_name)
                if folder_type.personal is True:
                    return False
                else:
                    folder_level = PasswordFolderACL.objects.get(folder__name=folder_name, user=request.user)
                    if folder_level.level.name in ['Owner', 'Admin']:
                        return True
                    else:
                        return False
            return True


class CanListPasswordFolderACL(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True


class CanRetrievePasswordFolderACL(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        try:
            folder = PasswordFolderACL.objects.get(id=obj.id).folder
            folder_level = PasswordFolderACL.objects.get(folder=folder, user=request.user)
        except PasswordFolderACL.DoesNotExist:
            return False
        if folder_level.level.name in ['Owner', 'Admin']:
            return True
        else:
            return False


class CanDestroyPasswordFolderACL(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.user is None:
            return False
        else:
            return True

# this needs to be fixed
# have to set false if acl is for the user trying to destroy
    def has_object_permission(self, request, view, obj):
        try:
            user = request.user
            acl_user = PasswordFolderACL.objects.get(id=obj.id).user
            if user == acl_user:
                return False
            else:
                return True
            level = get_permission_level(request, obj).level.name
        except AttributeError:
            return False
        if level in ['Owner']:
            return False
        else:
            return False