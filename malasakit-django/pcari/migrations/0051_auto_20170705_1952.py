# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-05 19:52
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcari', '0050_auto_20170702_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='language',
            field=models.CharField(blank=True, choices=[(b'en', 'English'), (b'tl', 'Filipino')], default='', max_length=8, validators=[django.core.validators.RegexValidator('^(|en|tl)$')]),
        ),
        migrations.AlterField(
            model_name='respondent',
            name='language',
            field=models.CharField(blank=True, choices=[(b'en', 'English'), (b'tl', 'Filipino')], default='', max_length=8, validators=[django.core.validators.RegexValidator('^(|en|tl)$')]),
        ),
    ]