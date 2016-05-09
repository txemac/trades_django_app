from rest_framework import serializers
from trades.models import Trade, Currency

__author__ = 'josebermudez'


class TradeCreateListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = '__all__'

    def validate(self, data):
        """
        Check sell amount positive.
        """
        if data['sell_amount'] < 0:
            raise serializers.ValidationError("Sell amount is negative.")
        if 'rate' in data and data['rate'] < 0.0:
            raise serializers.ValidationError("Rate is negative.")
        return data


class TradeEditSerializer(TradeCreateListSerializer):

    class Meta:
        model = Trade
        fields = '__all__'
        read_only_fields = ("sell_currency", "buy_currency", "buy_amount", "rate", "date_booked")


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'
