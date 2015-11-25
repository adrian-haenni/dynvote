# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20151122_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('interview_uuid', models.CharField(max_length=36, verbose_name=b'Interview unique identifier')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='choiceanswer',
            name='answer_ptr',
        ),
        migrations.RemoveField(
            model_name='question',
            name='answer_type',
        ),
        migrations.AddField(
            model_name='question',
            name='choices',
            field=models.TextField(help_text=b'if the question type is "radio," or "select,"', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(default=b'radio', max_length=200, choices=[(b'radio', b'radio'), (b'select', b'select')]),
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='AnswerRadio',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='home.AnswerBase')),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('home.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerSelect',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='home.AnswerBase')),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('home.answerbase',),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='ChoiceAnswer',
        ),
        migrations.AddField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(to='home.Survey'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='question',
            field=models.ForeignKey(to='home.Question'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='response',
            field=models.ForeignKey(to='home.Response'),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(to='home.Survey', null=True),
        ),
    ]
