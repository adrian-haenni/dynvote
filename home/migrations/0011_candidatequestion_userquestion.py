# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0010_response_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='home.Question')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            bases=('home.question',),
        ),
        migrations.CreateModel(
            name='UserQuestion',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='home.AnswerBase')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            bases=('home.answerbase',),
        ),
    ]
