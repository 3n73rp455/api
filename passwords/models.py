from django.db import models
from core.models import Owner, User
from passwordfolders.models import PasswordFolder
from taggit.managers import TaggableManager
from uuid import uuid4


class PasswordType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)

    class Meta:
        db_table = 'enterpass_passwordtype'
        managed = True

    def __str__(self):
        return self.name


class Password(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    type = models.ForeignKey(PasswordType, null=True, on_delete=models.PROTECT)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=1024)
    url = models.CharField(max_length=1024, null=True)
    folder = models.ForeignKey(PasswordFolder, on_delete=models.PROTECT)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'enterpass_password'
        managed = True

    def __str__(self):
        return self.name


class PasswordACL(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    password = models.ForeignKey(Password, on_delete=models.PROTECT)
    key = models.UUIDField(default=uuid4, unique=True)
    api = models.BooleanField(default=False, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)

    class Meta:
        db_table = 'enterpass_passwordacl'
        managed = True
