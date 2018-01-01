from core.models import User, AccessLevel, Owner, SystemSetting
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AccessLevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccessLevel
        fields = '__all__'


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class SystemSettingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SystemSetting
        fields = '__all__'
