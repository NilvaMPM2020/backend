from rest_framework import serializers

from account.models import User, Service, Round
from trades.models import Condition


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'name',
                  'avatar', 'rate', 'phone', 'email', 'user_type')
        read_only_fields = ('username', 'phone',)

    def get_avatar(self, obj):
        if not obj.avatar:
            return ''
        return obj.avatar.storage.base_location + '/' + obj.avatar.name


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ('id', 'title', 'description', 'checked')


class RoundSerializer(serializers.ModelSerializer):
    conditions = ConditionSerializer(many=True)

    class Meta:
        model = Round
        fields = ('id', 'name', 'duration', 'given_stock', 'got_stock', 'conditions')


class ServiceSerializer(serializers.ModelSerializer):
    rounds = RoundSerializer(many=True)

    class Meta:
        model = Service
        fields = ('id', 'name', 'avatar', 'description', 'rounds')


class LeanServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'avatar', 'description')
