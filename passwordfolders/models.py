from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from uuid import uuid4


class PasswordFolder(MPTTModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=1024)
    owner = models.ForeignKey('core.Owner', null=False, blank=False, default=1, on_delete=models.PROTECT)
    personal = models.BooleanField(null=False, blank=False, default=False)
    user = models.ForeignKey('core.User', null=True, blank=False, default=None, on_delete=models.PROTECT)
    parent = TreeForeignKey('self', null=True, blank=False, related_name='children', db_index=True, on_delete=models.DO_NOTHING)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=True)

    class MPTTMEta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'enterpass_passwordfolder'
        managed = True

    def __str__(self):
        return self.name


class PasswordFolderACL(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    folder = models.ForeignKey(PasswordFolder, on_delete=models.PROTECT)
    level = models.ForeignKey('core.AccessLevel', on_delete=models.PROTECT)
    key = models.UUIDField(default=uuid4, unique=True)
    modified = models.DateTimeField(auto_now=True, blank=False)

    class Meta:
        db_table = 'enterpass_passwordfolderacl'
        managed = True
