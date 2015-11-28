# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20151128_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='askbase',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='askbase',
            name='customQuestion',
            field=models.ForeignKey(to='home.Question', null=True),
        ),
        migrations.AlterField(
            model_name='askbase',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
