from django.contrib import admin
from trades.models import Trade, Currency


class TradeAdmin(admin.ModelAdmin):
    list_display = ("id", "date_booked")
    fields = ("sell_currency", "sell_amount", "buy_currency", "buy_amount", "rate", "date_booked")

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ("buy_amount", )
        return ("sell_currency", "buy_currency", "buy_amount", "rate", "date_booked")


admin.site.register(Trade, TradeAdmin)
admin.site.register(Currency)
