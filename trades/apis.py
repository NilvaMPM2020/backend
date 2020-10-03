from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from trades.models import Trade
from trades.serializers import TradeSerializer


class TradeAPI(generics.ListCreateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(service__business=self.request.user)
