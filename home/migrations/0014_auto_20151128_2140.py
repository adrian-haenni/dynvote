# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20151128_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='askbase',
            name='customQuestion',
            field=models.ForeignKey(to='home.CustomQuestion', null=True),
        ),
    ]
