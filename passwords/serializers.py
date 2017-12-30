from core.models import User
from passwords.models import Password, PasswordACL, PasswordType
from passwordfolders.models import PasswordFolder, PasswordFolderACL
from core.scripts.encryption import (decrypt_password,
                                     encrypt_password,
                                     generate_masterkey,
                                     generate_personalkey)
from rest_framework.serializers import ModelSerializer, SlugRelatedField, UUIDField
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from uuid import uuid4


class PasswordTypeSerializer(ModelSerializer):

    class Meta:
        model = PasswordType
        fields = ('name', 'description')


class PasswordACLSerializer(ModelSerializer):
    password = SlugRelatedField(
        queryset=Password.objects.all(),
        slug_field='id'
    )
    key = UUIDField(format='hex_verbose', default=uuid4())

    class Meta:
        model = PasswordACL
        fields = ('id', 'user', 'password', 'key', 'api')

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user

        super(PasswordACLSerializer, self).__init__(*args, **kwargs)
        try:
            placl = PasswordFolderACL.objects.select_related('folder').filter(user_id=user, level__name__in=['Owner', 'Admin'])
            folder_list = []
            for p in placl:
                folder_list.append(p.folder_id)
            self.fields['password'].queryset = Password.objects.filter(folder__in=folder_list)
        except (PasswordFolderACL.DoesNotExist, TypeError):
            self.fields['password'].queryset = None


class PasswordSerializer( ModelSerializer, TaggitSerializer):
    folder = SlugRelatedField(
        queryset=PasswordFolder.objects.all(),
        slug_field='name',
        default='Personal'
    )
    tags = TagListSerializerField()

    class Meta:
        model = Password
        fields = ('id', 'type', 'title', 'description', 'url', 'username', 'password', 'folder', 'tags', 'created',
                  'modified')

    def create(self, validated_data):
        user = User.objects.get(username=self.context['request'].user)
        validated_data['password'] = encrypt_password(generate_masterkey('28beatty'),
                                                   generate_personalkey(user.uuid, user.password),
                                                   validated_data['password'])
        password = super(PasswordSerializer, self).create(validated_data)
        return password

    def update(self, instance, validated_data):
        user = User.objects.get(username=self.context['request'].user)
        password = encrypt_password(generate_masterkey('28beatty'),
                                                   generate_personalkey(user.uuid, user.password),
                                                   validated_data.get('password', instance.password))
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.url = validated_data.get('url', instance.url)
        instance.username = validated_data.get('username', instance.username)
        instance.password = password
        instance.folder = validated_data.get('folder', instance.folder)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

    def to_representation(self, obj):
        user = User.objects.get(username=self.context['request'].user)
        if 'gAAA' in obj.password:
            obj.password = decrypt_password(generate_masterkey('28beatty'),
                                            generate_personalkey(user.uuid, user.password),
                                            obj.password)
        else:
            pass
        instance = super(PasswordSerializer, self).to_representation(obj)
        return instance


    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user

        super(PasswordSerializer, self).__init__(*args, **kwargs)
        try:
            placl = PasswordFolderACL.objects.select_related('folder').filter(user_id=user,
                                                                              level__name__in=['Owner', 'Admin'])
            folder_list = []
            for p in placl:
                folder_list.append(p.folder_id)
            self.fields['folder'].queryset = PasswordFolder.objects.filter(id__in=folder_list)
        except (PasswordFolderACL.DoesNotExist, TypeError):
            self.fields['folder'].queryset = None
