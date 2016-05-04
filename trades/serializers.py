from rest_framework import serializers
from trades.models import Trade, Currency

__author__ = 'josebermudez'


class TradeSerializer(serializers.ModelSerializer):

   class Meta:
       model = Trade
       fields = ("id", "sell_currency", "sell_amount", "buy_currency", "buy_amount", "rate", "date_booked")


class CurrencySerializer(serializers.ModelSerializer):

   class Meta:
       model = Currency
       fields = ("name",)
