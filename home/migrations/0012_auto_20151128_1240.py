# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0011_candidatequestion_userquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='AskBase',
            fields=[
                ('customQuestion', models.OneToOneField(primary_key=True, serialize=False, to='home.Question')),
                ('isAccepted', models.BooleanField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='CandidateQuestion',
            new_name='CustomQuestion',
        ),
        migrations.RemoveField(
            model_name='userquestion',
            name='answerbase_ptr',
        ),
        migrations.RemoveField(
            model_name='userquestion',
            name='creator',
        ),
        migrations.DeleteModel(
            name='UserQuestion',
        ),
    ]
