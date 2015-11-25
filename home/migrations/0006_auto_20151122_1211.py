# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20151101_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(default=b'None', max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='category_type',
            field=models.ForeignKey(to='home.Category', null=True),
        ),
    ]
