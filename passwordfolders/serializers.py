from core.models import AccessLevel, User
from passwordfolders.models import PasswordFolder, PasswordFolderACL
from rest_framework.serializers import ModelSerializer, SlugRelatedField, HiddenField
from rest_framework.validators import UniqueTogetherValidator
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer


class PasswordFolderACLSerializer(ModelSerializer):

    class Meta:
        model = PasswordFolderACL
        fields = ('id', 'modified', 'user', 'folder', 'level')

        validators = [
            UniqueTogetherValidator(
                queryset=PasswordFolderACL.objects.all(),
                fields=('user', 'folder', 'level')
            )
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user

        super(PasswordFolderACLSerializer, self).__init__(*args, **kwargs)
        try:
            placl = PasswordFolderACL.objects.select_related('folder').filter(user_id=user,
                                                                              level__name__in=['Owner', 'Admin'])
            folder_list = []
            for p in placl:
                folder_list.append(p.folder_id)
            self.fields['folder'].queryset = PasswordFolder.objects.filter(id__in=folder_list)
        except (PasswordFolderACL.DoesNotExist, TypeError):
            self.fields['folder'].queryset = None


class PasswordFolderSerializer(TaggitSerializer, ModelSerializer):
    tags = TagListSerializerField()

    def create(self, validated_data):
        request = self.context.get('request')
        owner = AccessLevel.objects.get(id=1)
        if validated_data['personal']:
            validated_data['user'] = request.user
        passwordfolder = PasswordFolder.objects.create(**validated_data)
        if request and hasattr(request, 'user'):
            user = request.user
            PasswordFolderACL.objects.create(user=user, folder=passwordfolder, level=owner)
        return passwordfolder

    class Meta:
        model = PasswordFolder
        fields = ('id', 'name', 'description', 'personal', 'parent', 'tags', 'created', 'modified')

        validators = [
            UniqueTogetherValidator(
                queryset=PasswordFolder.objects.all(),
                fields=('name', 'parent')
            )
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user

        super(PasswordFolderSerializer, self).__init__(*args, **kwargs)
        try:
            placl = PasswordFolderACL.objects.select_related('folder').filter(user_id=user)
            folder_list = []
            for p in placl:
                folder_list.append(p.folder_id)
            self.fields['parent'].queryset = PasswordFolder.objects.filter(id__in=folder_list)
        except (PasswordFolderACL.DoesNotExist, TypeError):
            self.fields['parent'].queryset = None
