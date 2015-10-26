# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_hands_judged'),
    ]

    operations = [
        migrations.CreateModel(
            name='Played',
            fields=[
                ('id', models.AutoField(max_length=b'10', serialize=False, primary_key=True)),
                ('playID', models.IntegerField(default=0)),
                ('handID', models.IntegerField(default=0)),
                ('wID', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
