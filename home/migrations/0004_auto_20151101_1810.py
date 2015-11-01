# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('home', '0003_auto_20151101_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=255)),
                ('answer_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='home.Answer')),
                ('answer', models.IntegerField(max_length=1, choices=[(0, 'Agree'), (1, 'Partially Agree'), (2, 'Partially Disagree'), (3, 'Disagree')])),
            ],
            bases=('home.answer',),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='home.Question'),
        ),
    ]
