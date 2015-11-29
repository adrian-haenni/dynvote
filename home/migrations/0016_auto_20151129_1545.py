# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_survey_surveypic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='surveypic',
            field=models.ImageField(default=b'survey_pictures/default.jpg', upload_to=b'/static/home/img/survey_pictures'),
        ),
    ]
