from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils import id_generator


class Currency(models.Model):
    name = models.CharField(_('Name'), max_length=255)

    def __unicode__(self):
        return self.name


class Trade(models.Model):
    id = models.CharField(primary_key=True, editable=False, default=id_generator, max_length=9)
    sell_currency = models.ForeignKey(Currency, verbose_name=_('Sell Currency'), related_name='sell_currency')
    sell_amount = models.DecimalField(verbose_name=_('Sell Amount'), max_digits=100, decimal_places=2)
    buy_currency = models.ForeignKey(Currency, verbose_name=_('Buy Currency'), related_name='buy_currency')
    buy_amount = models.DecimalField(verbose_name=_('Buy Amount'), max_digits=100, decimal_places=2)
    rate = models.DecimalField(verbose_name=_('Rate'), max_digits=5, decimal_places=4)
    date_booked = models.DateTimeField(verbose_name=_('Date Booked'), auto_now_add=True)

    def __unicode__(self):
        return self.id