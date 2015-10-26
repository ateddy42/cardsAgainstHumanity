# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20151026_0218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='handwhites',
            old_name='wid',
            new_name='wID',
        ),
    ]
