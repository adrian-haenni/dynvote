# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20151129_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='surveypic',
        ),
    ]
