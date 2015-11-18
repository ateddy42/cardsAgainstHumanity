# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20151116_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='judged',
            name='AIwin',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
