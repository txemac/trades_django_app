from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from trades.models import Trade
from trades.serializers import TradeCreateListSerializer, TradeEditSerializer, CurrencySerializer


class TradeListView(ListCreateAPIView):
    serializer_class = TradeCreateListSerializer
    queryset = Trade.objects.all()


class TradeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TradeEditSerializer
    queryset = Trade.objects.all()


class CurrencyCreateView(CreateAPIView):
    serializer_class = CurrencySerializer
    queryset = Trade.objects.all()
