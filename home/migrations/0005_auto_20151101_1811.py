# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20151101_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choiceanswer',
            name='answer',
            field=models.IntegerField(choices=[(0, 'Agree'), (1, 'Partially Agree'), (2, 'Partially Disagree'), (3, 'Disagree')]),
        ),
    ]
