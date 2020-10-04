# Create your views here.
from random import randint

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from MPM2020.settings import error_status
from MPM2020.utils import get_error_obj
from account.models import Service
from trades.models import Trade, Step, Condition, Judge
from trades.serializers import TradeSerializer


class TradeAPI(generics.ListCreateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 1:
            return self.queryset.filter(service__business=self.request.user)
        else:
            return self.queryset.filter(parties__in=[self.request.user])

    def create(self, request, *args, **kwargs):
        data = request.data
        service = Service.objects.filter(pk=data['service_id']).first()
        trade = Trade.objects.create(service=service)
        trade.parties.add(request.user)
        trade.parties.add(service.business)
        for r in service.rounds.all():
            step = Step.objects.create(name=r.name, duration=r.duration, given_stock=r.given_stock,
                                       got_stock=r.got_stock,
                                       trade=trade)
            for c in r.conditions.all():
                Condition.objects.create(title=c.title, description=c.description, related_step=step)
        price = int(service.rounds.all()[0].got_stock)
        if request.user.credit >= price:
            request.user.credit -= price
            request.user.save()
        else:
            return Response(get_error_obj(error_status['not_enough_credit']), status=status.HTTP_417_EXPECTATION_FAILED)
        return Response(TradeSerializer(trade).data)


class CancelAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, trade_id):
        if request.user.user_type == 0:
            reasons = request.data['reasons']
            trade = Trade.objects.filter(pk=trade_id).first()
            for reason in reasons:
                condition = Condition.objects.filter(trade=trade, pk=reason).first()
                condition.checked = True
                condition.save()
            trade.status = Trade.StatusChoices.WAITING_FOR_CANCELLATION_APPROVAL
            trade.save()
            return Response({'status': 'ok'})

        else:
            decision = request.data['decision']
            trade = Trade.objects.filter(pk=trade_id).first()
            if decision == 'accept':
                trade.status = Trade.StatusChoices.CANCELLED
                price = int(trade.steps.all()[0].got_stock)
                for party in trade.parties.all():
                    if party.pk is not request.user.pk:
                        party.credit += price
                        party.save()
                        break
            else:
                trade.status = Trade.StatusChoices.JUDGEMENT
            trade.save()
            return Response({'status': 'ok'})


class JudgeAPI(APIView):
    authentication_classes = [IsAuthenticated]

    def _finalize_decision(self, trade):
        vote = 0
        for judge in trade.judgements.all():
            vote += judge.decision
        if vote < 0:
            trade.status = Trade.StatusChoices.ACTIVE
            trade.save()
        else:
            trade.status = Trade.StatusChoices.ACTIVE
            price = int(trade.steps.all()[0].got_stock)
            for party in trade.parties.all():
                if party.pk is not self.request.user.pk:
                    party.credit += price
                    party.save()
                    break

    def post(self, request, trade_id):
        decision = request.data['decision']
        trade = Trade.objects.filter(pk=trade_id).first()
        Judge.objects.create(trade=trade, judge=request.user, decision=decision)
        if len(trade.judgements.all()) > 2:
            self._finalize_decision(trade)
        return Response({'status': 'ok'})

    def get(self, request):
        count = Trade.objects.filter(status=Trade.StatusChoices.JUDGEMENT).count()
        trade = Trade.objects.filter(status=Trade.StatusChoices.JUDGEMENT)[randint(0, count)]
        return Response(TradeSerializer(trade).data)
