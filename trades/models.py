from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
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
    buy_amount = models.DecimalField(verbose_name=_('Buy Amount'), max_digits=100, decimal_places=2, editable=False)
    rate = models.DecimalField(verbose_name=_('Rate'), max_digits=5, decimal_places=4)
    date_booked = models.DateTimeField(verbose_name=_('Date Booked'), auto_now_add=True)

    def __unicode__(self):
        return self.id


@receiver(pre_save, sender=Trade)
def calculate_amount(sender, instance, *args, **kwargs):
    instance.buy_amount = instance.sell_amount * instance.rate


@receiver(post_save, sender=Trade)
def send_email(sender, instance, *args, **kwargs):
    if settings.EMAIL_ENABLE:
        subject = "TradesApp - New trade"
        trade = instance

        email_context = {
            "trade": trade,
            "subject": subject
        }
        html_message = render_to_string("emails/new_trade.html", email_context)
        str_message = render_to_string("emails/new_trade.txt", email_context)

        from_email = settings.EMAIL_HOST_USER
        recipient_list = (settings.EMAIL_RECEIPT,)
        send_mail(subject=subject,
                  message=str_message,
                  from_email=from_email,
                  recipient_list=recipient_list,
                  html_message=html_message)
