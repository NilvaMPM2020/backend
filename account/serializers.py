from rest_framework import serializers

from account.models import User, Service, Round, ConditionSchema
from trades.models import Trade


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)
    trade_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'name',
                  'avatar', 'rate', 'phone',
                  'email', 'user_type', 'credit',
                  'trade_count')
        read_only_fields = ('username', 'phone', 'trade_count')

    def get_avatar(self, obj):
        if not obj.avatar:
            return ''
        return 'http://130.185.123.55/' + obj.avatar.storage.base_location + '/' + obj.avatar.name

    def get_trade_count(self, obj):
        return Trade.objects.filter(parties__username=obj.username).count()


class LeanUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'name',
                  'avatar', 'rate', 'user_type')
        read_only_fields = ('username', 'phone',)

    def get_avatar(self, obj):
        if not obj.avatar:
            return ''
        return obj.avatar.storage.base_location + '/' + obj.avatar.name


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionSchema
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
        read_only_fields = ('rounds', 'id', 'avatar', 'description')


class LeanServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'avatar', 'description')
