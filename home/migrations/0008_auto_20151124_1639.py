# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20151124_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='comments',
            field=models.TextField(null=True, verbose_name=b'Any additional Comments', blank=True),
        ),
        migrations.AddField(
            model_name='response',
            name='conditions',
            field=models.TextField(null=True, verbose_name=b'Conditions during interview', blank=True),
        ),
        migrations.AddField(
            model_name='response',
            name='interviewee',
            field=models.CharField(max_length=400, null=True, verbose_name=b'Name of Interviewee'),
        ),
        migrations.AddField(
            model_name='response',
            name='interviewer',
            field=models.CharField(max_length=400, null=True, verbose_name=b'Name of Interviewer'),
        ),
    ]
