# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.SmallIntegerField(choices=[(0, 'Agree'), (1, 'Partially Agree'), (2, 'Partially Disagree'), (3, 'Disagree')])),
                ('evaluation', models.ForeignKey(to='home.Evaluation')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationScheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='evaluationquestion',
            name='evaluation',
            field=models.ForeignKey(to='home.EvaluationScheme'),
        ),
        migrations.AddField(
            model_name='evaluationanswer',
            name='question',
            field=models.ForeignKey(to='home.EvaluationQuestion'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='scheme',
            field=models.ForeignKey(to='home.EvaluationScheme'),
        ),
    ]
