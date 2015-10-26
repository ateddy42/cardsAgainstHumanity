# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20151026_0320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hands',
            name='full',
        ),
        migrations.AddField(
            model_name='hands',
            name='numPlayed',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
