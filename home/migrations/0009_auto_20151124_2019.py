# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20151124_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='response',
            name='conditions',
        ),
        migrations.RemoveField(
            model_name='response',
            name='interviewee',
        ),
        migrations.RemoveField(
            model_name='response',
            name='interviewer',
        ),
    ]
