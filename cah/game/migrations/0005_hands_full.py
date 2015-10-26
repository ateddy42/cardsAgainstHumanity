# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20151026_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='hands',
            name='full',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
