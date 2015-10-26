# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20151026_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='judged',
            name='playerID',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
