# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hands',
            fields=[
                ('id', models.AutoField(max_length=b'10', serialize=False, primary_key=True)),
                ('bid', models.IntegerField(default=0)),
                ('w1', models.IntegerField(default=0)),
                ('w2', models.IntegerField(default=0)),
                ('w3', models.IntegerField(default=0)),
                ('w4', models.IntegerField(default=0)),
                ('w5', models.IntegerField(default=0)),
                ('w6', models.IntegerField(default=0)),
                ('w7', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Judged',
            fields=[
                ('id', models.AutoField(max_length=b'10', serialize=False, primary_key=True)),
                ('judgeID', models.IntegerField(default=0)),
                ('handID', models.IntegerField(default=0)),
                ('wID', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
