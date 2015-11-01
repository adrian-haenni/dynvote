# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20151030_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='scheme',
        ),
        migrations.RemoveField(
            model_name='evaluationanswer',
            name='evaluation',
        ),
        migrations.RemoveField(
            model_name='evaluationanswer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='evaluationquestion',
            name='evaluation',
        ),
        migrations.DeleteModel(
            name='Evaluation',
        ),
        migrations.DeleteModel(
            name='EvaluationAnswer',
        ),
        migrations.DeleteModel(
            name='EvaluationQuestion',
        ),
        migrations.DeleteModel(
            name='EvaluationScheme',
        ),
    ]
