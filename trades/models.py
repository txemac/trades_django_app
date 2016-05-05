from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from utils import id_generator


class Currency(models.Model):
    name = models.CharField(_('Name'), max_length=255)

    def __unicode__(self):
        return self.name


class Trade(models.Model):
    id = models.CharField(primary_key=True, editable=False, default=id_generator, max_length=9)
    sell_currency = models.ForeignKey(Currency, verbose_name=_('Sell Currency'), related_name='sell_currency', editable=False)
    sell_amount = models.DecimalField(verbose_name=_('Sell Amount'), max_digits=100, decimal_places=2)
    buy_currency = models.ForeignKey(Currency, verbose_name=_('Buy Currency'), related_name='buy_currency', editable=False)
    buy_amount = models.DecimalField(verbose_name=_('Buy Amount'), max_digits=100, decimal_places=2, editable=False)
    rate = models.DecimalField(verbose_name=_('Rate'), max_digits=5, decimal_places=4, editable=False)
    date_booked = models.DateTimeField(verbose_name=_('Date Booked'), auto_now_add=True)

    def __unicode__(self):
        return self.id


@receiver(pre_save, sender=Trade)
def my_callback(sender, instance, *args, **kwargs):
    instance.buy_amount = instance.sell_amount * instance.rate
