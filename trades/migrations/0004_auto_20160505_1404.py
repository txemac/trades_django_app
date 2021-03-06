# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-05 14:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0003_auto_20160505_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='buy_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_currency', to='trades.Currency', verbose_name='Buy Currency'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='rate',
            field=models.DecimalField(decimal_places=4, max_digits=5, verbose_name='Rate'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='sell_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sell_currency', to='trades.Currency', verbose_name='Sell Currency'),
        ),
    ]
