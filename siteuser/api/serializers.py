from rest_framework import serializers
from ..models import CustomUser, SiteUser, Role

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_active', 'last_login') # no email, for privacy purpose
        # fields = ('email', 'is_active', 'last_login')

class SiteUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    roles = serializers.CharField(source='get_all_roles', read_only=True)
    user = CustomUserSerializer()

    class Meta:
        model = SiteUser
        fields = ('user', 'first_name', 'last_name', 'screen_name', 'location', 'roles', 'url', 'avatar')

class RolesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ('name', )
