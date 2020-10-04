from rest_framework import serializers

from account.serializers import LeanServiceSerializer, LeanUserSerializer
from trades.models import Condition, Step, Trade


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ('id', 'title', 'description', 'checked')


class StepSerializer(serializers.ModelSerializer):
    conditions = ConditionSerializer(many=True)

    class Meta:
        model = Step
        fields = ('id', 'name', 'created_date', 'duration', 'given_stock', 'got_stock', 'conditions',
                  'judgement_description_business', 'description_client')


class TradeSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    parties = LeanUserSerializer(many=True)
    service = LeanServiceSerializer()

    class Meta:
        model = Trade
        fields = ('id', 'parties', 'service', 'steps', 'status')
