from django.db import models
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from uuid import uuid4

from .managers import UserManager
from passwordfolders.models import PasswordFolder, PasswordFolderACL


# Create a Personal Folder for the User when added to the System
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_personal_list(sender, instance=None, created=False, **kwargs):
    if created:
        owner = Owner.objects.get(name='Personal')
        PasswordFolder.objects.create(name='Personal',
                                      description='Personal Folder'.format(instance),
                                      owner=owner,
                                      personal=True,
                                      user=instance,
                                      parent=None)


class User(AbstractBaseUser, PermissionsMixin):
    is_superuser = models.BooleanField(default=False, editable=True)
    is_support = models.BooleanField(default=False, editable=True)
    is_servicedesk = models.BooleanField(default=False, editable=True)
    is_infosec = models.BooleanField(default=False, editable=True)
    is_application = models.BooleanField(default=False, editable=True)
    username = models.CharField(max_length=256, unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True, editable=True)
    last_login = models.DateField(auto_now=True)
    date_joined = models.DateField(auto_now=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def has_perm(self, perm, obj=None):
        return self.is_support

    def has_module_perms(self, app_label):
        return self.is_support

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def is_staff(self):
        return self.is_support

    class Meta:
        db_table = 'auth_user'
        managed = True
        verbose_name = 'user'
        verbose_name_plural = 'users'


class AccessLevel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)

    class Meta:
        db_table = 'auth_accesslevel'
        managed = True


class Owner(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)

    class Meta:
        db_table = 'core_owner'
        managed = True


class SystemSetting(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    value = models.CharField(max_length=1024)

    class Meta:
        db_table = 'core_systemsetting'
        managed = True

    def __str__(self):
        return self.name
