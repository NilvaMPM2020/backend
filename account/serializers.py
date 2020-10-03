from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'name',
                  'avatar', 'rate', 'phone', 'email', 'user_type')
        read_only_fields = ('username', 'phone',)

    def get_avatar(self, obj):
        if not obj.avatar:
            return ''
        return obj.avatar.storage.base_location + '/' + obj.avatar.name
