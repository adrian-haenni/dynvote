# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20151128_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='surveypic',
            field=models.ImageField(default=b'survey_pictures/default.jpg', upload_to=b'survey_pictures'),
        ),
    ]
