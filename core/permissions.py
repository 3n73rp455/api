from rest_framework import permissions


def is_support(request):
    try:
        if request.user.is_support:
            return True
    except AttributeError:
        return False


def is_servicedesk(request):
    try:
        if request.user.is_servicedesk:
            return True
    except AttributeError:
        return False


def is_superuser(request):
    try:
        if request.user.is_superuser:
            return True
    except AttributeError:
        return False


def is_application(request):
    try:
        if request.user.is_application:
            return True
    except AttributeError:
        return False


# User Permissions
class CanListUser(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanRetrieveUser(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanCreateUser(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanUpdateUser(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanDestroyUser(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False

# Access Level Permissions
class CanListAccessLevel(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanRetrieveAccessLevel(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanCreateAccessLevel(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanUpdateAccessLevel(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanDestroyAccessLevel(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


# Owner Permissions
class CanListOwner(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        return True


class CanRetrieveOwner(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        return True


class CanCreateOwner(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanUpdateOwner(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanDestroyOwner(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_servicedesk(request) is True or is_support(request) is True:
            return True
        else:
            return False


# System Setting Permissions
class CanListSystemSetting(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_superuser(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanRetrieveSystemSetting(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_superuser(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanCreateSystemSetting(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_superuser(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanUpdateSystemSetting(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_superuser(request) is True or is_support(request) is True:
            return True
        else:
            return False


class CanDestroySystemSetting(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        if is_superuser(request) is True or is_support(request) is True:
            return True
        else:
            return False