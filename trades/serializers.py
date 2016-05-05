from rest_framework import serializers
from trades.models import Trade, Currency

__author__ = 'josebermudez'


class TradeCreateListSerializer(serializers.ModelSerializer):

   class Meta:
       model = Trade
       fields = '__all__'


class TradeEditSerializer(serializers.ModelSerializer):

   class Meta:
       model = Trade
       fields = '__all__'
       read_only_fields = ("sell_currency", "buy_currency", "buy_amount", "rate", "date_booked")


class CurrencySerializer(serializers.ModelSerializer):

   class Meta:
       model = Currency
       fields = '__all__'
