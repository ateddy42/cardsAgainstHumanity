# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_hands_full'),
    ]

    operations = [
        migrations.CreateModel(
            name='HandWhites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('handID', models.IntegerField(default=0)),
                ('wid', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='hands',
            name='w1',
        ),
        migrations.RemoveField(
            model_name='hands',
            name='w2',
        ),
        migrations.RemoveField(
            model_name='hands',
            name='w3',
        ),
        migrations.RemoveField(
            model_name='hands',
            name='w4',
        ),
        migrations.RemoveField(
            model_name='hands',
            name='w5',
        ),
        migrations.RemoveField(
            model_name='hands',
            name='w6',
        ),
        migrations.RemoveField(
            model_name='hands',
            name='w7',
        ),
    ]
