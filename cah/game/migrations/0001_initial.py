# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlackCards',
            fields=[
                ('id', models.AutoField(max_length=b'4', serialize=False, primary_key=True)),
                ('text', models.TextField(default=b'', max_length=b'200')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WhiteCards',
            fields=[
                ('id', models.AutoField(max_length=b'4', serialize=False, primary_key=True)),
                ('text', models.TextField(default=b'', max_length=b'200')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
